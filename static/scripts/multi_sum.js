$(document).ready(function () {
    var clickedButtonValue = null;

    $('#inputForm').submit(function (e) {
        e.preventDefault();
        if (clickedButtonValue) {
            var formData = new FormData(this);
            formData.append('sub_button', clickedButtonValue);
            sendData('/load_content/multi_sum', formData);
        } else {
            console.log('No button clicked.');
        }
    });

    $('input[type="submit"]').click(function () {
        clickedButtonValue = $(this).val();
    });

    function sendData(url, data) {
        // AJAX 요청 시작 시 Loading 메시지 표시
        showLoading();

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function (data) {
                $('#content').html(data);
                hideLoading()
            },
            error: function () {
                $('#content').html('페이지를 불러오는 중 오류가 발생했습니다.');
                hideLoading()
            }
        });
    }

    // 서버 응답을 받을 때 Loading 메시지를 표시
    function showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    // 서버 응답을 받은 후 Loading 메시지를 숨김
    function hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }
});