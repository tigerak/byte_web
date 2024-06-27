$(document).ready(function () {

    // 하이라이트 표시
    var selectedHighlight = "";
    function updateRadioButtonState() {
        if (localStorage.getItem("highlight")) {
            selectedHighlight = localStorage.getItem("highlight");
            $("#" + selectedHighlight).prop("checked", true);
        }
    }

    // 각 라디오 버튼 클릭 이벤트 핸들러
    $('input[type="radio"]').click(function () {
        var name = $(this).attr("name");
        var value = $(this).attr("id");
        localStorage.setItem(name, value);
    });
    // 데이터 업데이트 버튼 클릭 시 라디오 버튼 상태 업데이트
    $('.sub_button').click(function () {
        updateRadioButtonState();
    });
    // 페이지 로드 시 라디오 버튼 상태 복원
    updateRadioButtonState();


    // 버튼 작동
    var clickedButtonValue = null;

    $('input[type="submit"]').click(function () {
        clickedButtonValue = $(this).val();
    });

    $('#inputForm').submit(function (e) {
        // div의 내용을 숨겨진 입력 필드에 복사
        var editableContent = $('#editableDiv').html();
        $('#hiddenInput').val(editableContent);
        
        e.preventDefault();
        if (clickedButtonValue) {
            var formData = new FormData(this);
            formData.append('sub_button', clickedButtonValue);
            sendData('/load_content/summary', formData);
        } else {
            console.log('No button clicked.');
        }
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
                // console.log('@@@ DATA @@@', data)
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