$(document).ready(function() {
    
    // // 커서 위치마다 엔터 기능 변경 
    // $('.searchDiv, .contentDiv').on('keypress', function(event) { 
    //     event.preventDefault(); // Prevent the 엔터의 default behavior (new line)
        
    //     if (event.key === 'Enter') {
            
    //         var divId = $(this).attr('id');
            
    //         if (divId === 'searchTag') {
    //             $('#getSearchDataButton').click();
    //         } else if (divId === 'searchCategory') {
    //             $('#getSearchDataButton').click();
    //         } else if (divId === 'modelSummary') {
    //             // 현재 커서 위치에 \n을 삽입
    //             insertTextAtCursor('\n');
    //         }
    //     }
    // });

    // // 커서 위치에 텍스트 삽입 함수
    // function insertTextAtCursor(text) {
    //     var sel, range;
    //     if (window.getSelection) {
    //         sel = window.getSelection();
    //         if (sel.getRangeAt && sel.rangeCount) {
    //             range = sel.getRangeAt(0);
    //             range.deleteContents();
                
    //             var textNode = document.createTextNode(text);
    //             range.insertNode(textNode);

    //             // 커서를 텍스트 끝에 위치시키기
    //             range.setStartAfter(textNode);
    //             range.setEndAfter(textNode);
    //             sel.removeAllRanges();
    //             sel.addRange(range);
    //         }
    //     }
    // }

    // 전역 변수를 선언하여 클릭된 collection_name 버튼ID를 저장합니다.
    var selectedBase = null;

    // DB 데이터 가져오기 버튼
    $('.getDataAPIButton').click(function() {
        showLoading();
        selectedBase = $(this).attr('id');
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: {getDataAPI: selectedBase,
                   buttonId: 'get_data'
            },
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
                        fetchArticleData(item.id, 'view-article');
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
    function fetchArticleData(id, buttonClass) {
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: { showIdData: id,
                getDataAPI: selectedBase,
                buttonId: buttonClass
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
                            // 줄바꿈 문자를 <br> 태그로 변환
                            if (typeof value === 'string') {
                                value = value.replace(/\n/g, '<br>');
                            }
                            // 해당 id를 가진 div에 값 설정
                            $('#' + key).html(value);
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

    // 저장 버튼 
    $('#saveButton').click(function() {
        showLoading();
        
        var buttonId = $(this).attr('id'); 
        var divs = $(this).data('divs').split(',');
        
        // 각 div에서 값을 추출하여 데이터를 구성
        var dataToSend = {};
        divs.forEach(function(divId) {
            var htmlContent = $('#' + divId).html(); 
            var textWithNewlines = htmlContent
            .replace(/<div>/gi, '\n')                // <div> 태그를 줄바꿈으로 변환
            .replace(/<\/div>/gi, '')               // </div> 태그를 제거
            .replace(/<br\s*\/?>/gi, '\n')          // <br> 태그를 줄바꿈으로 변환
            .replace(/&nbsp;/gi, ' ')               // &nbsp;를 공백으로 변환
            .replace(/<\/?[^>]+(>|$)/g, "");        // 남은 HTML 태그 제거

            dataToSend[divId] = textWithNewlines.trim(); // 양 끝의 공백 제거
        });
        // selectedBase 값을 추가
        dataToSend['getDataAPI'] = selectedBase;
        dataToSend['buttonId'] = buttonId;
    
        // AJAX POST 요청 보내기
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: dataToSend,
            success: function(response) {
                // $('.contentDiv').empty();
                $.each(response, function(key, value) {
                    $('#' + key).html(value);
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
    });



    // 삭제 버튼 
    $('#delButton').click(function() {
        var buttonId = $(this).attr('id'); 
        var divIds = $(this).data('divs').split(',');
        var formData = createFormData(divIds, buttonId);
        showLoading();
        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // $('.contentDiv').empty();
                $.each(response, function(key, value) {
                    $('#' + key).html(value);
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
    });

    function createFormData(divIds, buttonId) {
        // FormData 객체를 만듭니다.
        var formData = new FormData();

        // 각 div의 텍스트를 가져와 FormData 객체에 추가합니다.
        divIds.forEach(function(divId) {
            var divContent = $('#' + divId).text();
            formData.append(divId, divContent);
        });
        formData.append('getDataAPI', selectedBase);
        formData.append('buttonId', buttonId);
        return formData;
    }

    
    // API 테스트 버튼
    $('#getSearchDataButton').click(function() {
        showLoading();
        
        var buttonId = $(this).attr('id'); 
        var divs = $(this).data('divs').split(',');

        // 각 div에서 값을 추출하여 데이터를 구성
        var dataToSend = {};
        divs.forEach(function(divId) {
            var value = $('#' + divId).text(); // text()를 사용하여 div의 텍스트 내용 가져오기
            dataToSend[divId] = value;
        });
        
        // selectedBase 값을 추가
        dataToSend['getDataAPI'] = selectedBase;
        dataToSend['buttonId'] = buttonId;

        $.ajax({
            url: '/util/data_api',
            type: 'POST',
            data: dataToSend,
            success: function(response) {
                $('#getSearchDataDiv').empty();
                $.each(response, function(index, item) {
                    var index = $('<span>').addClass('index').text(String(item.index).padStart(4, '0') + '번');
                    var set_num = $('<span>').addClass('set_num').text('Set' + item.set_num + ' >> ');
                    var article_date = $('<span>').addClass('article_date').text(item.article_date + ' - ');
                    var title = $('<span>').addClass('title').text(item.title + ' ');
                    var viewArticleButton = $('<button>').addClass('view-article').text('기사 보기').click(function() {
                        $('#dbIdDiv').text(item.id); // #dbIdDiv에 id 넣기
                        fetchArticleData(item.id, 'view-article');
                    });
    
                    var itemDiv = $('<div>').addClass('item').append(index, set_num, article_date, title, viewArticleButton);
                    
                    // 아무데나 클릭 시 배경색 변경
                    itemDiv.click(function(e) {
                        if (!$(e.target).hasClass('view-article')) {
                            itemDiv.toggleClass('selected');
                        }
                    });
    
                    // 담기
                    $('#getSearchDataDiv').append(itemDiv);
                });
                hideLoading();
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
                hideLoading();
            }
        });
    });


    // 서버 응답을 받을 때 Loading 메시지를 표시
    function showLoading() {
        $('#loading').show();
    }
    // 서버 응답을 받은 후 Loading 메시지를 숨김
    function hideLoading() {
        $('#loading').hide();
    }    

});
