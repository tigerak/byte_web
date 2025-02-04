$(document).ready(function () {

    // url에 menu 확인 (DB 저장 화면에서 다른 화면 이동시에만 동작)
    var queryString = window.location.search;
    var urlParam = new URLSearchParams(queryString);
    var menu = urlParam.get("menu");
    if (menu != null) {
        $.ajax({
            url: '/load_content/' + menu + '?lastViewNumber=' + localStorage.getItem("lastViewNumber"),
            type: 'GET',
            success: function (data) {
                $('#content').html(data);
                // hideLoading()
            }
        });
    }


    // 메뉴 항목에 마우스가 올라갔을 때
    $('.menu-item').mouseenter(function () {
        $(this).css('color', '##9a1816ae'); // 텍스트 색상을 변경하거나 다른 스타일을 추가할 수 있습니다.
    });

    // 메뉴 항목에서 마우스가 떠날 때
    $('.menu-item').mouseleave(function () {
        $(this).css('color', ''); // 마우스가 떠날 때 스타일을 원래대로 복원합니다.
    });

    // 메뉴 항목 클릭 시
    $('#menu').on('click', '.menu-item', function () {
        var menu_item = $(this).data('menu-item');
        // AJAX 요청 시작 시 Loading 메시지 표시
        // showLoading();
        if (menu_item == "news_save") {
            location.href = "/news_save";
            /*$.ajax({
                url: '/load_content/' + menu_item + '?lastNewsNumber=' + localStorage.getItem("lastNewsNumber"),
                type: 'GET',
                success: function (data) {

                }
            });*/
        } else {
            $.ajax({
                url: '/load_content/' + menu_item + '?lastViewNumber=' + localStorage.getItem("lastViewNumber"),
                type: 'GET',
                success: function (data) {
                    $('#content').html(data);
                    // hideLoading()
                }
            });
        }

    });

    // 서버 응답을 받을 때 Loading 메시지를 표시
    function showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    // 서버 응답을 받은 후 Loading 메시지를 숨김
    function hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }
});