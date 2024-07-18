import os
import pwd
import grp

bind = 'unix:/var/run/gunicorn/gunicorn.sock'
workers = 1 # 모델 하나만 띄워야함.
reload = True # reload !!
timeout = 300
loglevel = 'info' # 'info' 'debug' # 로그 수준 설정

# 액세스 로그 파일 설정
accesslog = '-'  # '-'는 표준 출력을 의미합니다.
# 오류 로그 파일 설정
errorlog = '-'  # '-'는 표준 출력을 의미합니다.

umask = 0o007 # Unix 소켓 파일의 권한

# def post_fork(server, worker):
#     sock_file = '/var/run/gunicorn/gunicorn.sock'
#     # 소켓 파일의 소유자를 user_1로 설정
#     uid = pwd.getpwnam('web_ai').pw_uid
#     # 소켓 파일의 그룹을 www-data로 설정
#     gid = grp.getgrnam('www-data').gr_gid
#     # 소유자 및 그룹 설정
#     os.chown(sock_file, uid, gid)
#     # 권한 설정
#     os.chmod(sock_file, 0o660)