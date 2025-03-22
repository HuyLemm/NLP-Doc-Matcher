Cách chạy project:
1. Khởi động database PostgreSQL:
- Bước 1: Mở cmd với quyền admin
- Bước 2: pg_ctl -D "C:\Program Files\PostgreSQL\17\data" restart
- Bước 3: psql -U postgres
- Bước 4: Nhập password
* pg_ctl status: Check Status

2. Khởi động backend:
- Bước 1: cd backend
- Bước 2: python manage.py migrate
- Bước 3: python manage.py runserver

3. Khởi động frontend:
- Bước 1: cd frontend
- Bước 2: npm run dev
