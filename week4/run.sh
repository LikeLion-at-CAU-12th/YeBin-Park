lsof -t -i tcp:8000 | xargs kill -9
#8000 포트를 사용하는 모든 TCP 연결을 식별하고 해당하는 프로세스 ID 를 얻어 이를 kill -9 명령어로 강제종료
python manage.py runserver 0.0.0.0:8000