# 📝 Generador de Contratos Automatizado - Django

Este proyecto es una aplicación web desarrollada con Django que permite generar contratos en PDF de manera automática, a partir de un formulario simple con campos editables y checkboxes. Ideal para quienes necesitan crear múltiples contratos sin tener que redactarlos uno por uno.

## 🚀 Características

- Formulario dinámico con los siguientes campos:
  - Nombre del contratante
  - Fecha de inicio
  - Fecha de fin
  - ¿Requiere aval?
  - ¿Hay cuota de mantenimiento?
- Generación automática del contrato en PDF
- Botón para descargar el contrato listo para imprimir
- Funciona perfectamente en Render (hosting en la nube)
- No requiere dependencias complejas (usa `xhtml2pdf` en vez de WeasyPrint)

## 🖼️ Captura de pantalla

![Vista del formulario](https://github.com/tu-usuario/tu-repo/blob/main/static/img/captura_formulario.png)

> 🖼️ Cambia el link por el tuyo. Puedes guardar la imagen en la carpeta `static/img` y subirla a GitHub.

---

## 🛠️ Tecnologías usadas

- Django 5.x
- Python 3.x
- xhtml2pdf
- HTML5 + CSS3 (base)
- SQLite (default en Django)

---

## ⚙️ Cómo usarlo

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. Crea y activa el entorno virtual:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplica migraciones:
   ```bash
   python manage.py migrate
   ```

5. Corre el servidor local:
   ```bash
   python manage.py runserver
   ```

6. Accede a: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## ☁️ Despliegue en Render

1. Sube tu proyecto a GitHub.
2. En [Render.com](https://render.com/), crea un nuevo servicio **Web Service**.
3. Llena los datos del repositorio.
4. Usa estos comandos para el build:
   ```bash
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
5. Usa este comando para ejecutar:
   ```bash
   gunicorn contrato_auto.wsgi
   ```

---

## ✍️ Licencia

Este proyecto está bajo la licencia MIT. Puedes modificarlo y usarlo libremente.

---

## 📬 Contacto

¿Te gustaría integrar más funciones como firmas digitales, múltiples plantillas o integración con otros módulos?  
Contáctame para desarrollarlo juntos. 💼  
📧 ufkwear@gmail.com

