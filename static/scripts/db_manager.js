$(document).ready(function() {

    // 커서 위치마다 엔터 기능 변경 
    $('.contentDiv').on('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the 엔터의 default behavior (new line)
            var divId = $(this).attr('id');
            if (divId === 'urlDiv') {
                $('#scrapButton').click();
            } else if (divId === 'inputIdDiv') {
                $('#searchButton').click();
            } else if (divId === 'div3') {
                $('#button3').click();
            }
        }
    });


    // DB 데이터 가져오기 버튼
    $('#getDataAPIButton').click(function() {
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            success: function(response) {
                // 서버로부터 받은 데이터를 해당하는 div에 출력합니다.
                $('#getDataAPIDiv').empty();
                $.each(response, function(index, item) {
                    var checkbox = $('<input>').attr('type', 'checkbox').addClass('checkbox');
                    var set_num = $('<span>').addClass('set_num').text(item.set_num + '번 Set >> ');
                    var article_date = $('<span>').addClass('article_date').text(item.article_date + ' - ');
                    var title = $('<span>').addClass('title').text(item.title + ' ');
                    var viewArticleButton = $('<button>').addClass('view-article').text('기사 보기').click(function() {
                        $('#dbIdDiv').text(item.id); // #dbIdDiv에 id 넣기
                        fetchArticleData(item.url);
                    });
                    var url = $('<button>').addClass('url').text('원문 보기').click(function() {
                        window.open(item.url, '_blank');
                    });

                    var itemDiv = $('<div>').addClass('item').append(checkbox, set_num, article_date, title, viewArticleButton, url);
                    
                    // 아무데나 클릭 시 체크박스 선택
                    itemDiv.click(function(e) {
                        if (e.target.type !== 'checkbox' && !$(e.target).hasClass('view-article') && !$(e.target).hasClass('url')) {
                            var checkbox = $(this).find('.checkbox');
                            checkbox.prop('checked', !checkbox.prop('checked'));
                            itemDiv.toggleClass('checked', checkbox.prop('checked'));
                        }
                    });
                    // 체크박스 선택 시 배경색 변경
                    checkbox.change(function() {
                        itemDiv.toggleClass('checked', $(this).prop('checked'));
                    });
                    // 담기
                    $('#getDataAPIDiv').append(itemDiv);
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                $('#getDataAPIButton').html('페이지를 불러오는 중 오류가 발생했습니다.\n', error);
                hideLoading();
            }
        });
    });


    // '기사 보기' AJAX 요청을 보내는 함수
    function fetchArticleData(url) {
        showLoading();
        $.ajax({
            url: '/util/url_scraping',
            type: 'POST',
            data: { urlDiv: url },
            success: function(response) {
                $.each(response, function(key, value) {
                    if (value == null) {
                        return true; // continue와 같은 역할을 함. 다음 반복으로 넘어감
                    } else {
                        // 제일 앞의 개행 문자 제거
                        if (value.startsWith('\n')) {
                            value = value.substring(1);
                        }
                        // 해당 id를 가진 div에 값 설정
                        $('#' + key).text(value)
                    }
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
    }

    // 삭제 버튼 
    $('#delButton').click(function() {
        var divIds = $(this).data('divs').split(',');
        var formData = createFormData(divIds);
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#articleDiv').text(response.articleDiv);
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
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


    // 서버 응답을 받을 때 Loading 메시지를 표시
    function showLoading() {
        $('#loading').show();
    }
    // 서버 응답을 받은 후 Loading 메시지를 숨김
    function hideLoading() {
        $('#loading').hide();
    }    

});
