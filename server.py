from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Обработка GET-запросов (как ранее)
        try:
            with open('contacts.html', 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")

    def do_POST(self):
        # Обработка POST-запросов
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Декодирование и вывод данных
            decoded_data = post_data.decode('utf-8')
            print("\nReceived POST data:")
            print(decoded_data)

            # Парсинг данных формы (если нужно)
            form_data = parse_qs(decoded_data)
            if form_data:
                print("\nParsed form data:")
                for key, value in form_data.items():
                    print(f"{key}: {value[0]}")

            # Отправка ответа
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Data received successfully')

        except Exception as e:
            self.send_error(500, f"Error processing POST request: {str(e)}")


def run(server_class=HTTPServer, handler_class=SimpleServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
