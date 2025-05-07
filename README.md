# 🍔 RICCO BURGUER - Backend API

¡Bienvenido al repositorio del backend de **RICCO BURGUER**!  
Este sistema fue desarrollado con **Django** y **Django REST Framework**, y gestiona todo lo relacionado con la plataforma de RICCO BURGUER: usuarios, productos, compras, pedidos y más.

La API está diseñada para integrarse con dos clientes frontend:

- 💻 Una aplicación **web** desarrollada con **Angular 17**
- 📱 Una aplicación **mobile** desarrollada con **Java** en **Android Studio**

Repositorios de los frontends:

- [Frontend Mobile](https://github.com/G10-ISPC/Frontend-Mobile)
- [Frontend Web](https://github.com/G10-ISPC/Frontend-Web)

---

## 🎯 Propósito

El objetivo de Ricco Burgers es brindar a los pequeños negocios gastronómicos una plataforma propia de pedidos sin intermediarios ni comisiones. Esta solución digital permite gestionar productos, usuarios y pagos de forma centralizada, ágil y segura.

---

## 🚀 Tecnologías utilizadas

- **Python 3.x**
- **Django 4.x**
- **Django REST Framework**
- **MySQL** (o SQLite en desarrollo)
- **JWT** para autenticación
- **Mercado Pago SDK** (integración prevista)

---

## 📦 Instalación del proyecto

1. Clonar el repositorio:
```bash
git clone https://github.com/G10-ISPC/Ricco-Backend.git
cd Ricco-Backend

---

Crear entorno virtual e instalar dependencias:

python -m venv env
source env/bin/activate
pip install -r requirements.txt

---

Aplicar migraciones:

python manage.py migrate


---

Crear superusuario:

python manage.py createsuperuser

---

Ejecutar el servidor:

python manage.py runserver

---

🔐 Funcionalidades principales
Registro e inicio de sesión de usuarios

Roles diferenciados: cliente y administrador

CRUD de productos

Gestión de pedidos e historial de compras

Validación de datos sensibles

Panel de administración

API RESTful para integración con frontend web y mobile

---

📂 Estructura del proyecto

riccoburgers_backend/
├── api/                 # Apps de usuarios, productos, pedidos
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── riccoburgers/        # Configuración general del proyecto
├── manage.py
└── requirements.txt

---

📌 En desarrollo / mejoras futuras
Integración completa con Mercado Pago (modo sandbox y producción)

Exportación de pedidos a Excel

Dashboard con métricas de ventas

Sistema de promociones y fidelización

---

📘 Documentación complementaria

Autenticación basada en JWT

Rutas protegidas y validadas por rol

Consumo de esta API desde Angular y Android vía Axios/Fetch

---

📝 Licencia

Este proyecto es de uso libre para fines educativos y de aprendizaje.
Desarrollado en el marco del módulo Emprendedurismo y Tecnología y Desarrollo (ISPC – 2025).

---

🙌 Equipo de desarrollo

Este proyecto fue desarrollado por estudiantes del ISPC:

Carla Elizabeth Arévalo
Micaela Inés Juarez Manescotto
Delfina Aricoma
Ernesto Agustín Cevasco
Mariana Cos
Laura Patricia Cruz
Melisa Gulle
Dalma Florencia del Valle Ponce

---

Docentes responsables: Daniel Meloni y Salomon Yamil Eloy
