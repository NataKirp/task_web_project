import os
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def __get_static_file(self, file_path):
        """ Вспомогательный метод для чтения файлов из папки static """
        # Проверяем, существует ли такой файл на диске
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            # Задаем правильный тип
            if file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            if file_path.endswith('.js'):
                self.send_header('Content-type', 'text/javascript')
            if file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.send_header('Content-type', 'image/*')
            self.end_headers()
            # Читаем файлы из static в бинарном режиме
            with open(file_path, 'rb') as f:
                return f.read()
        return None

    def __get_contacts_page(self):
        """ Метод чтения и возврата страницы Контакты """
        with open('templates/contacts.html', 'r', encoding='utf-8') as f:
            return f.read()

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        # Обработка файлов из Static
        if self.path.startswith('/static/'):
            file_path = self.path.lstrip('/')
            static_content = self.__get_static_file(file_path)
            if static_content:
                self.wfile.write(static_content)
            else:
                self.send_error(404, 'File not found in Static directory')
            return
        # Обработка HTML-страницы
        elif self.path == "/" or self.path == '/contacts':
            page_content = self.__get_contacts_page()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(page_content, 'utf-8'))
            return
        else:
            self.send_error(404, 'Page not found')

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов со страницы контактов"""
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        print(body)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
