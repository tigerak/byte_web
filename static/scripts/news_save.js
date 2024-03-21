var secondaryCategories  = {
    '경제':['거시경제', '금융', '금리', '무역', '물가', '부동산', '세금', '원자재',
        '암호화폐', '보험', '재테크', '주식', '대출', '환율'],
    '산업':['인공지능', 'NFT', 'SNS', '메타버스', '모빌리티', '블록체인', '자율주행',
        '클라우드', '신기술', '금융업', '기업경영', '빅테크', '스타트업', '미디어',
        'OTT', '게임', '광고', '스포츠', '영화', '웹툰', '음악', '플랫폼', '바이오', '헬스케어',
        '뷰티', '유통', '에너지', '원자력', '정유업계', '천연가스', '친환경', '이동통신',
        '자동차', '디스플레이', '반도체', '이차전지', '스마트폰', '중공업', '의료', '전기차',
        '엔터테인먼트', '이커머스', '패션', '푸드', '건설', '공기업', '방산', '우주항공',
        '핀테크', '교육', '문화'],
    '국가':['미국', '일본', '중국', '유럽', '남미', '북미', '아프리카', '아시아',
        '오세아니아', '중동', '동남아시아', '전쟁', '외교']
};

$(document).ready(function () {

    $.each(secondaryCategories, function(category, items) {
        $.each(items, function (idx, item) {
            if (category == "경제") {
                $("#economy").append(
                    '<input type="checkbox" class="btn-check" id="' + item + '" autocomplete="off">'
                    + '<label class="btn btn-outline-primary m-1" for="' + item + '">' + item + '</label>'
                );
            } else if (category == "산업") {
                $("#industry").append(
                    '<input type="checkbox" class="btn-check" id="' + item + '" autocomplete="off">'
                    + '<label class="btn btn-outline-primary m-1" for="' + item + '">' + item + '</label>'
                );
            } else if (category == "국가") {
                $("#nation").append(
                    '<input type="checkbox" class="btn-check" id="' + item + '" autocomplete="off">'
                    + '<label class="btn btn-outline-primary m-1" for="' + item + '">' + item + '</label>'
                );
            }
        });
    });

    $(document).on("click", "#secondaryGroupModal input[type='checkbox']", function(e) {
        console.log(e.target);
    });

    $("#secondaryGroupModal .btn-check").click(
        (e) => {
            console.log(e.target.id)
            if ($(e.target).is(":checked")) {
                $("#secondaryGroup").append(
                    '<input type="checkbox" class="btn-check" id="' + e.target.id + 'copy" autocomplete="off" checked disabled>'
                    + '<label class="btn btn-outline-primary m-1" id="' + e.target.id + 'copyLabel" for="' + e.target.id + 'copy">' + e.target.id + '</label>'
                )
            } else {
                $("#" + e.target.id + "copy").remove();
                $("#" + e.target.id + "copyLabel").remove();
            }
        });


    $("#primaryGroupModal .btn-check").click(
        (e) => {

            if ($(e.target).is(":checked")) {
                $("#primaryGroup").append(
                    '<input type="checkbox" class="btn-check" id="' + e.target.id + 'copy" autocomplete="off" checked disabled>'
                    + '<label class="btn btn-outline-primary m-1" id="' + e.target.id + 'copyLabel" for="' + e.target.id + 'copy">' + e.target.id + '</label>'
                )
            } else {
                $("#" + e.target.id + "copy").remove();
                $("#" + e.target.id + "copyLabel").remove();
            }
    });

    $("#category").change(
        (e) => {
            const selectedValue = $(e.target).val();
            if (selectedValue == '직접 입력') {
                $("#category").addClass('display-none');
                $("#customInput").removeClass('display-none');
                $("#cancel").removeClass('display-none');
            }
    });

    $("#cancel").click(
        (e) => {
            $("#category").removeClass('display-none');
            $("#customInput").addClass('display-none');
            $("#cancel").addClass('display-none');
            $("#category option:eq(0)").prop('selected', true);
    });

    $(".nav-link").click(
        (e) => {
            console.log(e.target.dataset.value)
            var menu_item = e.target.dataset.value;
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
                location.href = "/";
                $.ajax({
                    url: '/load_content/' + menu_item + '?lastNewsNumber=' + localStorage.getItem("lastNewsNumber"),
                    type: 'GET',
                    success: function (data) {
                        $('#content').html(data);
                        // hideLoading()
                    }
                });
            }

    });

    $("#getNews").click(
        (e) => {
            const url = $("#inputUrl").val();
            if (url == '') {
                alert('URL을 입력해주세요.');
                return
            }

            $.ajax({
                url: "/getNews?url=" + url,
                type: "GET",
                success: function (res) {
                    if (res == '실패') {
                        alert('기사를 가져오는데 실패했습니다. URL을 확인 해 주세요.');
                        return;
                    } else {
                        $("#title").val(res.title);
                        $("#media").val(res.media);
                        $("#article_date").val(res.article_date);
                        $("#article").val(res.article);
                    }
                },
                error: function (res) {
                    console.log(res);
                }
            })
        });

});
