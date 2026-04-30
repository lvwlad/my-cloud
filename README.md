my-cloud/
├── docker-compose.yml
│
├── backend/
│   ├── .env                       
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py                
│       ├── auth.py                
│       ├── files.py               
│       ├── models.py               
│       └── database.py             
│
├── backend/storage/                
│   └── {user_id}/
│       └── {папки и файлы}/
│
└── frontend/
    ├── login.html
    ├── files.html
    ├── css/
    │   └── style.css
    └── js/
        ├── api.js                 
        ├── login.js                
        └── files.js                