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

    // 기사 수집 버튼
    $('#scrapButton').click(function() {
        // 클릭된 버튼의 data-divs 속성 값을 가져옵니다.
        var divIds = $(this).data('divs').split(',');
        // FormData 객체를 생성하고 데이터 추가
        var formData = createFormData(divIds);
        // content-div 모두 제거
        $('.contentDiv').empty();
        $(".dropbtn").text("관계 설정");
            selectedRelation = "";
        // 데이터를 서버로 전송합니다.
        sendData('/util/url_scraping', formData);
    });

    

    // 완성된 json 가져오는 API로 연결되는 버튼
    $('#get-data-API-button').click(function() {
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            success: function(data) {
                // 서버로부터 받은 데이터를 해당하는 div에 출력합니다.
                $('#get-data-API-box').empty();
                $.each(data, function(index, item) {
                    var checkbox = $('<input>').attr('type', 'checkbox').addClass('checkbox');
                    var set_num = $('<span>').addClass('set_num').text(item.set_num + '번 Set >> ');
                    var article_date = $('<span>').addClass('article_date').text(item.article_date + ' - ');
                    var title = $('<span>').addClass('title').text(item.title + ' ');
                    var viewArticleButton = $('<button>').addClass('view-article').text('기사 보기').click(function() {
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
                    // 출력
                    $('#get-data-API-box').append(itemDiv);
                    hideLoading();
                });
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
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
                $('#titleDiv').text(response.titleDiv);
                $('#categoryDiv').text(response.categoryDiv || ''); // 카테고리가 없을 수 있으므로 기본값 처리
                $('#mediaDiv').text(response.mediaDiv);
                $('#dateDiv').text(response.dateDiv);
                $('#articleDiv').text(response.articleDiv);
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
    }

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
                $.each(response, function(index, item) {
                    var set_num = $('<span>').addClass('set_num').text(item.set_num + '번 Set >> ');
                    var article_date = $('<span>').addClass('article_date').text(item.article_date + ' - ');
                    var title = $('<span>').addClass('title').text(item.title + ' ');
                    var url = $('<button>').addClass('url').text('기사보기').click(function() {
                        window.open(item.url, '_blank');
                    });

                    var itemDiv = $('<div>').addClass('item').append(set_num, article_date, title, url);
                    $('#get-api-box').append(itemDiv);
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                // index의 #content 임.
                $('#get-api-box').html('페이지를 불러오는 중 오류가 발생했습니다.');
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
