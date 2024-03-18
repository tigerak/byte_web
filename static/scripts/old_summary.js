$(document).ready(function () {
    var selectedModel = "";
    var selectedSummaryWay = "";
    var selectedProof = "";

    function updateRadioButtonState() {
        if (localStorage.getItem("model")) {
            selectedModel = localStorage.getItem("model");
            $("#" + selectedModel).prop("checked", true);
        }
        if (localStorage.getItem("summary_way")) {
            selectedSummaryWay = localStorage.getItem("summary_way");
            $("#" + selectedSummaryWay).prop("checked", true);
        }
        if (localStorage.getItem("proof")) {
            selectedProof = localStorage.getItem("proof");
            $("#" + selectedProof).prop("checked", true);
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

    var clickedButtonValue = null;

    $('#inputForm').submit(function (e) {
        e.preventDefault();
        if (clickedButtonValue) {
            var formData = new FormData(this);
            formData.append('sub_button', clickedButtonValue);
            sendData('/load_content/summary', formData);
        } else {
            console.log('No button clicked.');
        }
    });

    $('input[type="submit"]').click(function () {
        clickedButtonValue = $(this).val();
    });

    // #extract_topic 버튼 클릭 이벤트 핸들러
    $('#extract_topic').click(function () {
        var articleText = $('#article_text').val(); // #article_text에서 텍스트 추출
        var titleText = $('#title_text').val()

        // FormData 객체 생성
        var formData = new FormData();
        formData.append('sub_button', $('#extract_topic').val());
        formData.append('title_text', titleText); // FormData에 article_text 필드 추가
        formData.append('article_text', articleText); // FormData에 article_text 필드 추가

        // sendData 함수 호출, '/your_endpoint'는 적절한 서버 엔드포인트로 대체
        sendData('/load_content/summary', formData);
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