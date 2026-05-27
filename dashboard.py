import http.server
import socketserver
import sqlite3
import json
import os
import sys
import urllib.parse
import webbrowser
import threading
import time

# Target port and file paths
PORT = 8050
DB_NAME = "FinalDB.db"
HTML_NAME = "index.html"

# Resolve absolute paths in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
HTML_PATH = os.path.join(BASE_DIR, HTML_NAME)

def get_db_connection():
    """Establish a connection to the SQLite database with Row factory."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"El archivo de base de datos '{DB_NAME}' no se encuentra en {BASE_DIR}. Ejecuta el notebook para crearlo.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_valid_tables(conn):
    """Retrieve lists of tables from the database to validate inputs."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    return [row['name'] for row in cursor.fetchall()]

def get_table_columns(conn, table_name):
    """Retrieve lists of columns for a specific table."""
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info("{table_name}")')
    return [row['name'] for row in cursor.fetchall()]

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Override to suppress console spam
        pass

    def send_json(self, data, status=200):
        """Helper to send JSON response."""
        response_bytes = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        """CORS preflight request support."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Route: Serve Homepage
        if path in ('/', '/index.html'):
            try:
                with open(HTML_PATH, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error cargando index.html: {str(e)}")
            return

        # Route: /api/tables
        if path == '/api/tables':
            try:
                conn = get_db_connection()
                tables = get_valid_tables(conn)
                result = []
                for t in tables:
                    cursor = conn.cursor()
                    cursor.execute(f'SELECT COUNT(*) FROM "{t}"')
                    count = cursor.fetchone()[0]
                    result.append({"name": t, "count": count})
                conn.close()
                self.send_json({"tables": result})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # Route: /api/table_data
        if path == '/api/table_data':
            try:
                query_params = urllib.parse.parse_qs(parsed_url.query)
                table = query_params.get('table', [None])[0]
                limit = int(query_params.get('limit', [25])[0])
                offset = int(query_params.get('offset', [0])[0])
                search = query_params.get('search', [''])[0]
                sort = query_params.get('sort', [None])[0]
                order = query_params.get('order', ['ASC'])[0].upper()

                if not table:
                    return self.send_json({"error": "Parámetro 'table' es requerido"}, 400)

                conn = get_db_connection()
                valid_tables = get_valid_tables(conn)
                
                # Input validation to prevent SQL Injection on dynamic table names
                if table not in valid_tables:
                    conn.close()
                    return self.send_json({"error": f"Tabla inválida: {table}"}, 400)

                columns = get_table_columns(conn, table)

                # Base query and params
                where_clause = ""
                params = []

                if search:
                    # Construct search for text matching across all columns
                    search_conditions = []
                    for col in columns:
                        search_conditions.append(f'"{col}" LIKE ?')
                        params.append(f"%{search}%")
                    where_clause = " WHERE " + " OR ".join(search_conditions)

                # Get total count with search filter
                count_query = f'SELECT COUNT(*) FROM "{table}"' + where_clause
                cursor = conn.cursor()
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]

                # Data query with sort/pagination
                data_query = f'SELECT * FROM "{table}"' + where_clause
                
                if sort:
                    # Validate sort column
                    if sort in columns and order in ('ASC', 'DESC'):
                        data_query += f' ORDER BY "{sort}" {order}'

                data_query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])

                cursor.execute(data_query, params)
                rows = [dict(r) for r in cursor.fetchall()]
                
                conn.close()
                self.send_json({
                    "columns": columns,
                    "rows": rows,
                    "total_count": total_count
                })
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # Not Found
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/query':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data)
                sql_query = data.get('sql', '').strip()

                if not sql_query:
                    return self.send_json({"error": "La consulta SQL no puede estar vacía"}, 400)

                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Execute user statement
                cursor.execute(sql_query)
                
                if cursor.description is not None:
                    # It's a query returning rows (e.g. SELECT)
                    columns = [desc[0] for desc in cursor.description]
                    rows = [dict(row) for row in cursor.fetchall()]
                    conn.close()
                    self.send_json({
                        "columns": columns,
                        "rows": rows
                    })
                else:
                    # It's a command (e.g. UPDATE, INSERT, CREATE)
                    conn.commit()
                    rowcount = cursor.rowcount
                    conn.close()
                    self.send_json({
                        "columns": ["message"],
                        "rows": [{"message": f"Consulta ejecutada con éxito. Filas afectadas: {rowcount}"}]
                    })
            except sqlite3.Error as e:
                self.send_json({"error": f"Error de SQLite: {str(e)}"}, 200) # Send DB error message to client display
            except Exception as e:
                self.send_json({"error": f"Error del servidor: {str(e)}"}, 500)
            return

        self.send_response(404)
        self.end_headers()


def open_browser():
    """Wait for server to start, then open the default browser."""
    time.sleep(1.0)
    print(f"\nAbriendo el navegador en http://localhost:{PORT} ...")
    webbrowser.open(f"http://localhost:{PORT}")


if __name__ == "__main__":
    # Check database file
    if not os.path.exists(DB_PATH):
        print(f"\n[ERROR] No se encontró la base de datos SQLite '{DB_NAME}' en:")
        print(f"  {DB_PATH}")
        print("\nPor favor ejecuta primero las celdas del archivo 'mod5_final_project.ipynb'")
        print("para descargar los archivos CSV e importar las tablas en la base de datos.")
        sys.exit(1)

    # Allow custom port from command argument
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            pass

    # Setup local server
    handler = DashboardHandler
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("="*60)
        print(f" Servidor iniciado en http://localhost:{PORT}")
        print(f" Base de Datos activa: {DB_PATH}")
        print(f" Presiona CTRL+C en la consola para detener el servidor.")
        print("="*60)
        
        # Start browser thread
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")
            httpd.server_close()
            sys.exit(0)
