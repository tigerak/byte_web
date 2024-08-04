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


    // 전역 변수를 선언하여 클릭된 collection_name 버튼ID를 저장합니다.
    var selectedBase = null;

    // DB 데이터 가져오기 버튼
    $('.getDataAPIButton').click(function() {
        showLoading();
        selectedBase = $(this).attr('id');
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: {getDataAPI: selectedBase},
            success: function(response) {
                // 서버로부터 받은 데이터를 해당하는 div에 출력합니다.
                $('#getDataAPIDiv').empty();
                $.each(response, function(index, item) {
                    var index = $('<span>').addClass('index').text(String(item.index).padStart(4, '0') + '번');
                    var checkbox = $('<input>').attr('type', 'checkbox').addClass('checkbox');
                    var set_num = $('<span>').addClass('set_num').text('Set' + item.set_num + ' >> ');
                    var article_date = $('<span>').addClass('article_date').text(item.article_date + ' - ');
                    var title = $('<span>').addClass('title').text(item.title + ' ');
                    var viewArticleButton = $('<button>').addClass('view-article').text('기사 보기').click(function() {
                        $('#dbIdDiv').text(item.id); // #dbIdDiv에 id 넣기
                        fetchArticleData(item.id);
                    });
                    var url = $('<button>').addClass('url').text('원문 보기').click(function() {
                        window.open(item.url, '_blank');
                    });

                    var itemDiv = $('<div>').addClass('item').append(index, checkbox, set_num, article_date, title, viewArticleButton, url);
                    
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
                $('#getDataAPIDiv').html('페이지를 불러오는 중 오류가 발생했습니다.\n', error);
                hideLoading();
            }
        });
    });


    // '기사 보기' AJAX 요청을 보내는 함수
    function fetchArticleData(id) {
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: { showIdData: id,
                getDataAPI: selectedBase
             },
            success: function(response) {
                // contentDiv class를 가진 div를 깨끗하게 지움
                $('.contentDiv').empty();
                $.each(response, function(key, value) {
                    if (value == null) {
                        // value가 null인 경우 빈 문자열 설정
                        $('#' + key).text('');
                        return true; // continue와 같은 역할을 함. 다음 반복으로 넘어감
                    } else {
                        // value가 문자열인지 확인한 후 처리
                        if (typeof value === 'string' && value.startsWith('\n')) {
                            value = value.substring(1);
                        }
                        
                        // key가 similarityDiv인 경우
                        if (key === 'similarityDiv') {
                            // value가 null 또는 undefined인 경우 빈 문자열 설정
                            if (value == null) {
                                $('#' + key).text('');
                            } else if (Array.isArray(value)) {
                                // value가 배열인 경우 항목을 추가
                                // value가 2차원 배열로 들어오므로, 각 배열의 항목을 처리
                                $.each(value, function(index, item) {
                                    // item이 배열로 들어오는 경우
                                    var indexSpan = $('<span>').addClass('index').text(String(item[0]).padStart(4, '0') + '번');
                                    var checkbox = $('<input>').attr('type', 'checkbox').addClass('checkbox');
                                    var setNumSpan = $('<span>').addClass('set_num').text('Set' + item[1] + ' >> ');
                                    var scoreSpan = $('<span>').addClass('score').text('Score: ' + item[2]);

                                    var itemDiv = $('<div>').addClass('item').append(indexSpan, checkbox, setNumSpan, scoreSpan);

                                    // 아무데나 클릭 시 체크박스 선택
                                    itemDiv.click(function(e) {
                                        if (e.target.type !== 'checkbox') {
                                            checkbox.prop('checked', !checkbox.prop('checked'));
                                            itemDiv.toggleClass('checked', checkbox.prop('checked'));
                                        }
                                    });

                                    // 체크박스 선택 시 배경색 변경
                                    checkbox.change(function() {
                                        itemDiv.toggleClass('checked', $(this).prop('checked'));
                                    });
                                    
                                    // 만들어진 div를 similarityDiv에 추가
                                    $('#' + key).append(itemDiv);
                                });
                            } else {
                                console.error('Expected array for similarityDiv, but received:', value);
                            }
                        } else {
                            // 해당 id를 가진 div에 값 설정
                            $('#' + key).text(value);
                        }
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
        formData.append('getDataAPI', selectedBase);
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
