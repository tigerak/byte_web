$(document).ready(function() {
    // 커서 위치마다 엔터 기능 변경 
    $('.contentDiv').on('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the 엔터의 default behavior (new line)
            var divId = $(this).attr('id');
            if (divId === 'urlDiv') {
                $('#scrapButton').click();
            } else if (divId === 'inputIdDiv') {
                $('#searchBut').click();
            } else if (divId === 'div3') {
                $('#button3').click();
            }
        }
    });

    // 스크래핑 버튼
    $('#scrapButton').click(function() {
        // 클릭된 버튼의 data-divs 속성 값을 가져옵니다.
        var divIds = $(this).data('divs').split(',');
        // FormData 객체를 생성하고 데이터 추가
        var formData = createFormData(divIds);
        // content-div 클래스를 가진 모든 div의 텍스트를 지웁니다.
        $('.contentDiv').text('');
        // 데이터를 서버로 전송합니다.
        sendData('/util/url_scraping', formData);
    });

    // 요약 버튼
    $('#summaryButton').click(function() {
        var divIds = $(this).data('divs').split(',');
        var formData = createFormData(divIds);
        sendData('/util/model_api', formData);
    });

    function createFormData(divIds) {
        // FormData 객체를 만듭니다.
        var formData = new FormData();

        // 각 div의 텍스트를 가져와 FormData 객체에 추가합니다.
        divIds.forEach(function(divId) {
            var divContent = $('#' + divId).text();
            formData.append(divId, divContent);
        });

        return formData;
    }

    function sendData(url, formData) {
        showLoading();

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // 서버로부터 받은 데이터를 해당하는 div에 출력합니다.
                $.each(response, function(key, value) {
                    // 제일 앞의 개행 문자 제거
                    if (value.startsWith('\n')) {
                        value = value.substring(1);
                    }
                    // 해당 id를 가진 div에 값 설정
                    $('#' + key).text(value).css('white-space', 'pre-wrap');  // .text()를 사용하여 텍스트 설정하고, 인라인 스타일 추가
                });
                // Loding 메시지 제거
                hideLoading();
            },
            error: function(xhr, status, error) {
                // index의 #content 임.
                $('#content').html('페이지를 불러오는 중 오류가 발생했습니다.');
                hideLoading();
            }
        });
    }

    // 서버 응답을 받을 때 Loading 메시지를 표시
    function showLoading() {
        $('#loading').show();
    }

    // 서버 응답을 받은 후 Loading 메시지를 숨김
    function hideLoading() {
        $('#loading').hide();
    }
});
