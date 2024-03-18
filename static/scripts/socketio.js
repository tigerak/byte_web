document.addEventListener('DOMContentLoaded', () => {
    // 소켓 접속
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    console.log('일단 접속' + 'http://' + document.domain + ':' + location.port + '/test');

    // 그냥 환영
    socket.on('connect', function() {
        console.log('어?');
        const kind = '알 림';
        const noti = '### 접 속 @ 완 료 ###';
        socket.emit('test_message', {name:kind, text:noti});
        console.log('됏나?');
    });

    // @socketio.on('test_message') 로부터 받음.
    socket.on('output_message', data => {
        console.log(`송신자 : ${data['name']}`); // 따옴표 아님
        console.log(`수신 메시지 : ${data['text']}`); // 따옴표 아님

        const br = document.createElement('br');
        const span_userame = document.createElement('span')
        const p = document.createElement('p');
        span_userame.innerHTML = data['name'];

        p.innerHTML = span_userame.outerHTML + ' : ' + data['text'] + br.outerHTML;

        document.querySelector('#display_message_section').append(p);
    });

    // 그냥 샘플
    // socket.on('some_event', data => {
    //     console.log(data)
    // });

    // 메시지 전송
    const messageInput = document.getElementById('user_message');
    const usernameInput = document.getElementById('user_name') || '익명';
    const sendButton = document.getElementById('send_button');

    sendButton.addEventListener('click', function() {
        const message = messageInput.value;
        const username = usernameInput.value;

        if (message.trim() !== '') {
            socket.emit('test_message', { name:username, text:message });
            
            messageInput.value = '';
            messageInput.focus(); // 메시지를 전송한 후에도 커서를 messageInput 입력란에 설정합니다.
        } else {
            console.error('메시지를 입력하세요.');
        }

        return false;
    });

    // 엔터 키 눌렀을 때 sendButton 클릭 이벤트 발생
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            sendButton.click(); // sendButton을 클릭합니다.
            event.preventDefault(); // 엔터 키에 의한 기본 동작을 막습니다.
        }
    });
});