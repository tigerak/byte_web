$(document).ready(function () {

    // // AJAX 요청이 이미 성공적으로 완료되었는지 확인
    // var isDataFetched = localStorage.getItem('isDataFetched');

    // // localStorage에서 lastVisitNumber 값 가져오기
    // var lastVisitNumber = localStorage.getItem('lastVisitNumber') || "1";
    
    // // 데이터가 아직 가져오지 않았고, lastVisitNumber가 있는 경우에만 AJAX 요청 실행
    // if (!isDataFetched && lastVisitNumber) {
    //     $.ajax({
    //         url: '/load_content/mod_db', // 서버의 엔드포인트 URL
    //         type: 'GET', // 요청 방식
    //         data: {dbid: lastVisitNumber}, // 서버에 전달할 데이터
    //         success: function(data) {
    //             $('#content').html(data); // 데이터로 페이지 내용 업데이트
    //             hideLoading();

    //             // AJAX 요청 성공 플래그를 localStorage에 설정
    //             localStorage.setItem('isDataFetched', 'true');
    //         },
    //         error: function(xhr, status, error) {
    //             console.log("Error fetching data: " + error);
    //         }
    //     });
    // }



    // 드롭다운 메뉴
    var selectedRelation = ""; // 사용자가 선택한 관계를 저장하는 변수
    var firstCompanyRole = "main"; // 기본적으로 firstCompany는 main으로 설정
    var secondCompanyRole = "sub"; // 기본적으로 secondCompany는 sub으로 설정
  
    $(".dropdown-content a").click(function(e){
        e.preventDefault(); // 기본 이벤트 방지
        selectedRelation = $(this).text(); // 선택한 관계 업데이트
        $(".dropbtn").text(selectedRelation); // 버튼 텍스트를 선택한 항목으로 변경
        $(".dropdown-content").hide(); // 드롭다운 메뉴 닫기
    });

    $("#addButton").click(function(){
        var firstCompany  = $("#firstCompany ").text().trim();
        var secondCompany  = $("#secondCompany ").text().trim();
        
        // 하나 이상의 필드가 채워져 있는지 확인
        if(firstCompany || selectedRelation || secondCompany) {
            var data = {};
            // 존재하는 필드만 데이터 객체에 추가
            if (firstCompany) data['first-' + firstCompanyRole] = firstCompany;
            if (selectedRelation) data.relation = selectedRelation;
            if (secondCompany) data['second-' + secondCompanyRole] = secondCompany;
            // 새 div에 데이터 추가
            var dataItem = $("<div class='data-item'>" + JSON.stringify(data) + "<span class='delete-btn'>삭제</span></div>");
            dataItem.appendTo("#companyTagContainer");
            
            // 삭제 버튼 이벤트 리스너 설정
            // dataItem.find(".delete-btn").click(function() {
            //     $(this).parent().remove(); // 해당 항목 삭제
            // });
        } else {
            alert("적어도 하나의 필드를 채워주세요.");
        }
    });
    
    // 삭제 버튼에 대한 이벤트 위임 설정
    $("#companyTagContainer").on("click", ".delete-btn", function() {
        $(this).parent().remove(); // 해당 항목 삭제
    });

    $(".dropbtn").click(function(){
        $(".dropdown-content").toggle();
    });

    // main/sub 선택 버튼
    $(".toggle-btn").click(function() {
        var target = $(this).data('target');
        if ($(target).attr('id') === "firstCompany") {
            firstCompanyRole = (firstCompanyRole === "main" ? "sub" : "main");
            $(this).text(firstCompanyRole === "main" ? "Main" : "Sub"); // 토글 버튼의 텍스트 업데이트
        } else {
            secondCompanyRole = (secondCompanyRole === "main" ? "sub" : "main");
            $(this).text(secondCompanyRole === "main" ? "Main" : "Sub");
        }
        
    });

    // 외부 클릭 시 드롭다운 메뉴 닫기
    $(document).click(function(e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown-content').hide();
        }
    });



    // 카테고리 데이터
    var primaryCategories = {
        '대분류': ['경제', '비즈니스', '사회']
    };
    var secondaryCategories  = {
        '경제':['거시경제', '금융', '금리', '무역', '물가', '부동산', '세금', '원자재', 
                '암호화폐', '보험', '재테크', '주식', '대출', '환율'],
        '산업':['인공지능', 'NFT', 'SNS', '메타버스', '모빌리티', '블록체인', '자율주행', 
                '클라우드', '신기술', '금융업', '기업경영', '빅테크', '스타트업', '미디어', 
                'OTT', '게임', '광고', '스포츠', '영화', '웹툰', '음악', '플랫폼', '바이오', '헬스케어', 
                '뷰티', '유통', '에너지', '원자력', '정유업계', '천연가스', '친환경', '이동통신', 
                '자동차', '디스플레이', '반도체', '이차전지', '스마트폰', '중공업', '의료', '전기차',  
                '엔터테인먼트', '이커머스', '패션', '푸드', '건설', '공기업', '방산', '우주항공',
                '핀테크', '교육', '문화', '가전', '웨어러블', '소부장(소재/부품/장비)', '전자', '로봇',
                '소프트웨어' ],
        '국가':['미국', '일본', '중국', '유럽', '남미', '북미', '아프리카', '아시아', 
                '오세아니아', '중동', '동남아시아', '전쟁', '외교']
    };
    var selected = {
        'primary': [],
        'secondary': []
    };

    // 카테고리 모달 생성 함수
    function createCategoryModal(categories, modalId, selectedDivId) {
        var modal = $(modalId);
        $.each(categories, function(category, items) {
            var categoryDiv = $('<div>').addClass('category');
            $('<h3>').text(category).appendTo(categoryDiv);
            $.each(items, function(index, item) {
                $('<span>').addClass('category-item').text(item).click(function() {
                    $(this).toggleClass('selected');
                    updateSelectedCategories(modalId, selectedDivId);
                }).appendTo(categoryDiv);
            });
            categoryDiv.appendTo(modal.find('.categories'));
        });
    }

    // 선택된 카테고리 업데이트 함수
    function updateSelectedCategories(modalId, selectedDivId) {
        var selectedItems = $(modalId + ' .selected').map(function() {
            return $(this).text();
        }).get();
        var selectedKey = modalId.includes('primary') ? 'primary' : 'secondary';
        selected[selectedKey] = selectedItems;

        // 선택된 항목을 각각의 span으로 감싸 박스 형태로 표시
        $(selectedDivId).empty(); // 이전에 선택된 항목을 비웁니다.
        $.each(selectedItems, function(index, item) {
            $('<span>').addClass('selected-item').text(item).appendTo(selectedDivId);
        });
    }

    //////////////////////////////////////////////////////////////
    // 1차 카테고리 모달 초기화
    createCategoryModal(primaryCategories, '#primaryCategoryModal', '#selectedPrimaryCategories');
    $('#openPrimaryModal').click(function() {
        $('#primaryCategoryModal').show();
    });

    // 2차 카테고리 모달 초기화
    createCategoryModal(secondaryCategories, '#secondaryCategoryModal', '#selectedSecondaryCategories');
    $('#openSecondaryModal').click(function() {
        $('#secondaryCategoryModal').show();
    });
    //////////////////////////////////////////////////////////////

    //////////////////////////////////////////////////////////////
    // 모달 열기 버튼 클릭 이벤트. 이벤트 버블링 방지 추가
    $('#openPrimaryModal, #openSecondaryModal').click(function(event) {
        event.stopPropagation(); // 이벤트 버블링 방지
        var targetModal = $(this).data('target'); // data-target 속성을 사용해 모달 선택
        $(targetModal).show();
    });

    // 모달 내부 클릭 시 이벤트 버블링 방지
    $('.modal').click(function(event) {
        event.stopPropagation(); // 모달 내부 클릭 시 이벤트 버블링 방지
    });

    // 외부 클릭 시 모달 닫기
    $(document).click(function() {
        $('.modal').hide(); // 모든 모달을 숨깁니다.
    });
    //////////////////////////////////////////////////////////////

    // 모달 닫기
    $('.close-modal').click(function() {
        $(this).closest('.modal').hide();
    });



    // 기존 요약문 가져오기 버튼
    $("#copy_sum").click(function() {
        // 'id="SumDiv"'인 <div>에서 HTML 내용을 가져옵니다.
        var summaryTitleContent = $("#sumTitDiv").html();
        var summaryContent = $("#sumDiv").html();
        // 가져온 텍스트 내용을 <div>에 설정합니다.
        $("#modTitDiv").html(summaryTitleContent);
        $("#modSumDiv").html(summaryContent);
    });



    // 버튼 작동
    var clickedButtonValue = null;

    $('input[type="submit"]').click(function () {
        clickedButtonValue = $(this).val();
    });

    // 저장 버튼 클릭 이벤트
    $('#save_but').click(function() {
        var lastSaveNumber = $('#currentNewsNumber').text();
        localStorage.setItem('lastSaveNumber', lastSaveNumber);
        console.log(localStorage.getItem("lastSaveNumber") + " : lastSaveNumber");
    });

    // targetDBid 버튼 클릭 시 DB Id 저장
    $('#searchBut').click(function() {
        var lastVisitNumberText = $('#title_text').text(); // 버튼의 텍스트 값을 가져옴
        var lastVisitNumberMatches = lastVisitNumberText.match(/\d+/); // 숫자만 추출
        var lastVisitNumber = lastVisitNumberMatches ? lastVisitNumberMatches[0] : "1"; // 매치된 숫자가 있으면 사용하고, 없으면 "1"을 기본값으로 사용

        var lastViewNumber = $('#title_text').val();
        localStorage.setItem('lastViewNumber', lastViewNumber);
        console.log(localStorage.getItem("lastViewNumber") + " : lastViewNumber");

    });

    // prevBut 버튼 클릭 시 DB Id 저장
    $('#prevBut').click(function() {
        var lastVisitNumberText = $('#prevDiv').text(); // prevDiv의 텍스트 값을 가져옴
        var lastVisitNumberMatches = lastVisitNumberText.match(/\d+/); // 숫자만 추출
        var lastVisitNumber = lastVisitNumberMatches ? lastVisitNumberMatches[0] : "1"; // 매치된 숫자가 있으면 사용하고, 없으면 "1"을 기본값으로 사용

        localStorage.setItem('lastViewNumber', lastVisitNumber);
        console.log(localStorage.getItem("lastViewNumber") + " : lastViewNumber")
    });

    // nextBut 버튼 클릭 시 DB Id 저장
    $('#nextBut').click(function() {
        var lastVisitNumberText = $('#nextDiv').text(); // 버튼의 텍스트 값을 가져옴
        var lastVisitNumberMatches = lastVisitNumberText.match(/\d+/); // 숫자만 추출
        var lastVisitNumber = lastVisitNumberMatches ? lastVisitNumberMatches[0] : "1"; // 매치된 숫자가 있으면 사용하고, 없으면 "1"을 기본값으로 사용

        localStorage.setItem('lastViewNumber', lastVisitNumber);
        console.log(localStorage.getItem("lastViewNumber") + " : lastViewNumber")
    });

    // HTML 특수 기호 제거 함수.
    function decodeHTMLEntities(text) {
        const textarea = document.createElement('textarea');
        textarea.innerHTML = text;
        return textarea.value;
    }

    // 폼 제출 이벤트
    $('#searchForm').submit(function (e) {
        e.preventDefault();
        if (clickedButtonValue) {
            var formData = new FormData(this);
            formData.append('sub_button', clickedButtonValue);

            var modSumContent = decodeHTMLEntities($('#modSumDiv').html());
            $('#hiddenModSum').val(modSumContent);
            var modTitContent = decodeHTMLEntities($('#modTitDiv').html());
            $('#hiddenModTit').val(modTitContent);
            var modReaContent = decodeHTMLEntities($('#modReaDiv').html());
            $('#hiddenModRea').val(modReaContent);
            var prevContent = $('#prevDiv').html();
            $('#hiddenPrev').val(prevContent);
            var nextContent = $('#nextDiv').html();
            $('#hiddenNext').val(nextContent);
            var companyTagContent = '';
            $('#companyTagContainer .data-item').each(function(index, element) {
                var itemText = $(this).clone() // 요소 복제
                                    .find('.delete-btn').remove().end() // '삭제' 버튼 제거
                                    .text().trim(); // 텍스트 추출 및 앞뒤 공백 제거
                // 마지막 항목이 아니면 텍스트 뒤에 쉼표와 공백 추가
                if (index < $('#companyTagContainer .data-item').length - 1) {
                    companyTagContent += itemText + ', ';
                } else {
                    // 마지막 항목인 경우 그냥 텍스트 추가
                    companyTagContent += itemText;
                }
            });
            var primaryTagContent = $('#selectedPrimaryCategories .selected-item').map(function() {
                return $(this).text().trim(); // 각 '.selected-item'의 텍스트 추출 및 앞뒤 공백 제거
            }).get().join(', '); // 배열을 문자열로 변환, 각 항목 사이에 쉼표와 공백 추가
            var secondaryTagContent = $('#selectedSecondaryCategories .selected-item').map(function() {
                return $(this).text().trim(); // 각 '.selected-item'의 텍스트 추출 및 앞뒤 공백 제거
            }).get().join(', '); // 배열을 문자열로 변환, 각 항목 사이에 쉼표와 공백 추가

            formData.append('mod_sum', modSumContent);
            formData.append('mod_sum_tit', modTitContent);
            formData.append('mod_rea', modReaContent);
            formData.append('prev_num', prevContent);
            formData.append('next_num', nextContent);
            formData.append('company_tag', companyTagContent);
            formData.append('primary_tag', primaryTagContent);
            formData.append('secondary_tag', secondaryTagContent);

            formData.append('lastViewNumber', localStorage.getItem("lastViewNumber"));

            if (localStorage.getItem("lastSaveNumber") == null) {
                formData.append('lastSaveNumber', 0);
            } else {
                formData.append('lastSaveNumber', localStorage.getItem("lastSaveNumber"));
            }

            formData.append('currentNewsNumber', $("#currentNewsNumber").text());

            sendData('/load_content/mod_db', formData);
        } else {
            console.log('No button clicked.');
        }
    });

    // 엔터 키가 눌렸을 때 "검색" 버튼 클릭 처리
    $('#searchForm input').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
            $('input[type="submit"].sub_button[value="검색"]').click();
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
                var lastViewNumber =$(data).find("#currentNewsNumber").text();
                localStorage.setItem('lastViewNumber', lastViewNumber);
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