var secondaryCategories  = {
    '경제':['거시경제', '금융', '금리', '무역', '물가', '부동산', '세금', '원자재',
        '암호화폐', '보험', '재테크', '주식', '대출', '환율'],
    '산업':['인공지능', 'NFT', 'SNS', '메타버스', '모빌리티', '블록체인', '자율주행',
        '클라우드', '신기술', '금융업', '기업경영', '빅테크', '스타트업', '미디어',
        'OTT', '게임', '광고', '스포츠', '영화', '웹툰', '음악', '플랫폼', '바이오', '헬스케어',
        '뷰티', '유통', '에너지', '원자력', '정유업계', '천연가스', '친환경', '이동통신',
        '자동차', '디스플레이', '반도체', '이차전지', '스마트폰', '중공업', '의료', '전기차',
        '엔터테인먼트', '이커머스', '패션', '푸드', '건설', '공기업', '방산', '우주항공',
        '핀테크', '교육', '문화', '가전', '웨어러블', '소부장(소재/부품/장비)', '전자'],
    '국가':['미국', '일본', '중국', '유럽', '남미', '북미', '아프리카', '아시아',
        '오세아니아', '중동', '동남아시아', '전쟁', '외교']
};

$(document).ready(function () {

    $("#changeBtn2").click(
        (e) => {
            if ($(e.target).data('value') == 'main') {
                $(e.target).html("sub")
                $(e.target).data('value', 'sub')
            } else {
                $(e.target).html("main")
                $(e.target).data('value', 'main')
            }
        }
    )

    $("#changeBtn1").click(
        (e) => {
            if ($(e.target).data('value') == 'main') {
                $(e.target).html("sub")
                $(e.target).data('value', 'sub')
            } else {
                $(e.target).html("main")
                $(e.target).data('value', 'main')
            }
        }
    )



    // 삭제 버튼에 대한 클릭 이벤트 추가
    $('#companyTagList').on('click', '.relationDelete', function() {
        // 현재 삭제 버튼이 속한 input-group 요소를 찾아서 삭제
        $(this).closest('.input-group').remove();
    });

    $("#add").click(
        (e) => {
            /*const mainCompany = $("#mainCompany").val();
            const subCompany = $("#subCompany").val();*/
            const first = $("#first").val();
            const second = $("#second").val();
            const firstValue = $("#changeBtn1").data('value');
            const secondValue = $("#changeBtn2").data('value');
            const relation = $("#relation").val();

            if(first || relation || second) {
                var data = {};
                // 존재하는 필드만 데이터 객체에 추가
                if (first) data['first-' + firstValue] = first;
                if (relation) data.relation = relation;
                if (second) data['second-' + secondValue] = second;

                const relationDataString = JSON.stringify(data).replace(/"/g, '&quot;');
                // 새 div에 데이터 추가
                $("#companyTagList").append(
                    '<div class="input-group mb-3">' +
                    '<input type="text" class="form-control" placeholder="" aria-label="" aria-describedby="basic-addon1" readonly=""' +
                    'value="' + relationDataString + '">' +
                    '<button class="btn btn-primary relationDelete" type="button">삭제</button>' +
                    '</div>'
                );

            } else {
                alert("적어도 하나의 필드를 채워주세요.");
            }

        }
    )

    $("#saveModalBtn").click(
        (e) => {
            location.reload(true);
        }
    )

    $("#save").click(
        (e) => {

            const inputUrl = $("#inputUrl").val();
            const title = $("#title").val();
            const media = $("#media").val();
            const articleDate = $("#articleDate").val();
            /*const category = $("#category").val();*/
            const article = $("#article").val();
            const summaryTitle = $("#summaryTitle").val();
            // const summary = $("#summary").val();
            // const modifiedReason = $("#modifiedReason").val();

            const summary = $("#summary").val().replace(/(?:\r\n|\r|\n)/g, '\n');
            const modifiedReason = $("#modifiedReason").val().replace(/(?:\r\n|\r|\n)/g, '\n');


            const companyTag = [];
            $("#companyTagList input").each(function() {
                const parsedObject = JSON.parse($(this).val());
                companyTag.push(parsedObject);
            });

            const primaryTag = [];
            $("#primaryGroup label").each(function() {
                primaryTag.push($(this).text());
            });

            const secondaryTag = [];
            $("#secondaryGroup label").each(function() {
                secondaryTag.push($(this).text());
            });
            const data = [{
                "articleDate" : articleDate,
                "media" : media,
                "url" : inputUrl,
                /*"category" : category,*/
                "title" : title,
                "article" : article,
                "modifiedSummaryTitle" : summaryTitle,
                "modifiedSummary" : summary,
                "modifiedReason" : modifiedReason,
                "companyTag" : companyTag,
                "primaryTag" : primaryTag.toString(),
                "secondaryTag" : secondaryTag
            }];

            // 유효성 검사
            if (inputUrl == "") {
                alert("URL을 입력해주세요.")
                return;
            }

            if (title == "") {
                alert("뉴스 기사를 검색해주세요.")
                return;
            }

            /*if (category == "") {
                alert("카테고리를 입력해주세요.")
                return;
            }*/


            $.ajax({
                url: "/save",
                type: "POST",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                data: JSON.stringify(data),
                success: function (res) {
                    if (res.result.message != null) {
                        alert("DB에 저장되었습니다. DB 번호 : " + res.result.message);
                        location.href = "/news_save";
                    }

                },
                error: function (res) {
                    alert("저장에 실패하였습니다.")
                }
            });
        });

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


    $("#economy, #industry, #nation .btn-check").click(
        (e) => {

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

            $("#primaryGroup").html(
                '<input type="checkbox" class="btn-check" id="' + e.target.id + 'copy" autocomplete="off" checked disabled>'
                + '<label class="btn btn-outline-primary m-1" id="' + e.target.id + 'copyLabel" for="' + e.target.id + 'copy">' + e.target.id + '</label>'
            )

            /*if ($(e.target).is(":checked")) {
                $("#primaryGroup").append(
                    '<input type="checkbox" class="btn-check" id="' + e.target.id + 'copy" autocomplete="off" checked disabled>'
                    + '<label class="btn btn-outline-primary m-1" id="' + e.target.id + 'copyLabel" for="' + e.target.id + 'copy">' + e.target.id + '</label>'
                )
            } else {
                $("#" + e.target.id + "copy").remove();
                $("#" + e.target.id + "copyLabel").remove();
            }*/
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
            if (menu_item == "news_save") {
                location.href = "/news_save";
            } else {
                location.href = "/?menu=" + menu_item;
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
                        $("#articleDate").val(res.article_date);
                        $("#article").val(res.article);
                    }
                },
                error: function (res) {
                    console.log(res);
                }
            })
        });

});
