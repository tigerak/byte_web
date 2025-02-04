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

    // AWS DB에 연결되는 버튼
    $('.aws-db-but').click(function() {
        var divIds = $(this).data('divs');
        var formData;

        // formData 생성
        if (typeof divIds === 'string') {
            divIds = divIds.split(',');
            formData = createFormData(divIds);
        } else {
            formData = new FormData(); 
        }
        
        // 클릭한 버튼의 id 추가
        formData.append('buttonId', $(this).attr('id'));

        // #delButton 클릭 시 나머지 코드 실행하지 않고 바로 전송
        if ($(this).attr('id') === 'delButton') {
            if (confirm('정말 삭제하시겠습니까?')) { // 확인 팝업
                sendData('/util/aws_db_api', formData);
            }
            return;
        }

        // 마지막 본 기사 버튼을 클릭한 경우 lastViewNumber 추가
        if ($(this).attr('id') === 'listVisitButton') {
            var lastViewNumber = localStorage.getItem('lastViewNumber');
            if (lastViewNumber) {
                formData.append('lastViewNumber', lastViewNumber);
            }
        }

        // 마지막 본 기사 localStorage에 저장
        var lastVisitNumberText = $('#dbIdDiv').text(); // prevDiv의 텍스트 값을 가져옴
        var lastVisitNumberMatches = lastVisitNumberText.match(/\d+/); // 숫자만 추출
        var lastVisitNumber = lastVisitNumberMatches ? lastVisitNumberMatches[0] : "1"; // 매치된 숫자가 있으면 사용하고, 없으면 "1"을 기본값으로 사용

        localStorage.setItem('lastViewNumber', lastVisitNumber);
        // 마지막 저장한 기사로 저장

        // 화면 초기화
        $('.contentDiv').empty();
        $(".dropbtn").text("관계 설정");
            selectedRelation = "";
        
        // 전송
        sendData('/util/aws_db_api', formData);
    });

    // Model Broker로 연결되는 버튼
    $('#summaryButton').click(function() {
        showLoading();
        var divIds = $(this).data('divs').split(',');
        var formData = createFormData(divIds);
        // 서버에 작업 요청을 보내고, task_id를 받아옴
        $.ajax({
            url: '/util/broker_q',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    const task_id = response.task_id;
                    const q_len = response.q_len;
                    updateProgress(`작업이 대기열에 추가되었습니다. 현재 대기 중인 작업 수: ${q_len}`);
                    checkJobStatus(task_id);  // 작업 상태 확인 시작
                } else {
                    alert('Failed to start job: ' + response.status);
                }
            },
            error: function(xhr, status, error) {
                alert('Error: ' + error);
            }
        });
    });

    function checkJobStatus(task_id) {
        // 5초마다 서버에 상태를 요청하는 함수
        const intervalId = setInterval(function() {
            $.ajax({
                url: '/util/job_status',
                method: 'POST',
                data: { 'task_id': task_id },
                success: function(response) {
                    
                    if (response.status === 'success') {
                        // 작업이 완료된 경우 결과를 처리하고 폴링 중지
                        clearInterval(intervalId);
                        updatePageWithResult(response.result);
                        hideLoading();
                    } else if (response.status === 'error') {
                        // 작업이 실패한 경우 오류 메시지를 표시하고 폴링 중지
                        clearInterval(intervalId);
                        alert('Job failed: ' + response.message);
                        hideLoading();
                    } else {
                        // 작업이 아직 진행 중인 경우 상태를 표시
                        updateProgress(response.message);
                    }
                },
                error: function(xhr, status, error) {
                    // 요청 중 에러 발생 시 폴링 중지
                    clearInterval(intervalId);
                    alert('Error: ' + error);
                    hideLoading();
                }
            });
        }, 5000); // 5초마다 서버에 요청
    }

    function updateProgress(message) {
        // 페이지에서 작업 진행 상태를 표시하는 함수
        $('#modelSummary').text(message);
    }

    function updatePageWithResult(result) {
        // 작업이 완료된 후 결과를 페이지에 표시하는 함수
        $.each(result, function(key, value) {
            // 해당 id를 가진 div에 값 설정
            $('#' + key).text(value).css('white-space', 'pre-wrap');
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
                $.each(response, function(key, value) {
                    // value가 null 또는 undefined 인 경우 건너뛰기
                    if (value == null) {
                        return true; // continue와 같은 역할을 함. 다음 반복으로 넘어감
                    }

                    // #companyTagContainer
                    if (key === 'companyTag' && Array.isArray(value)) {
                        $("#companyTagContainer").empty();

                        value.forEach(function(tag) {
                            var data = {};
                            if (tag['first-main']) data['first-main'] = tag['first-main'];
                            if (tag['first-sub']) data['first-sub'] = tag['first-sub'];
                            if (tag.relation) data.relation = tag.relation;
                            if (tag['second-main']) data['second-main'] = tag['second-main'];
                            if (tag['second-sub']) data['second-sub'] = tag['second-sub'];
    
                            var dataItem = $("<div class='data-item'>" + JSON.stringify(data) + "<span class='delete-btn'>삭제</span></div>");
                            dataItem.appendTo("#companyTagContainer");
                        });

                    // #selectedPrimaryCategories
                    } else if (key === 'primaryTag') {
                        if (value !== '') {
                            // primaryTag를 출력
                            $('#selectedPrimaryCategories').empty(); // 이전에 선택된 항목을 비웁니다.
                            $('<span>').addClass('selected-item').text(value).appendTo('#selectedPrimaryCategories');
                            selected.primary = [value]; // selected 객체 업데이트
                        }
                    // #selectedSecondaryCategories
                    } else if (key === 'secondaryTag' && Array.isArray(value)) {
                        // secondaryTag를 출력
                        $('#selectedSecondaryCategories').empty(); // 이전에 선택된 항목을 비웁니다.
                        value.forEach(function(item) {
                            $('<span>').addClass('selected-item').text(item).appendTo('#selectedSecondaryCategories');
                        });
                        selected.secondary = value; // selected 객체 업데이트
                    // etc.
                    } else {
                        // 제일 앞의 개행 문자 제거
                        if (value.startsWith('\n')) {
                            value = value.substring(1);
                        }
                        // 해당 id를 가진 div에 값 설정
                        $('#' + key).text(value).css('white-space', 'pre-wrap');  // .text()를 사용하여 텍스트 설정하고, 인라인 스타일 추가
                    }
                });
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


    ////////////////////////////// 회사 관계 태그 //////////////////////////////
    var selectedRelation = ""; // 사용자가 선택한 관계를 저장하는 변수
    var firstCompanyRole = "main"; // 기본적으로 firstCompany는 main으로 설정
    var secondCompanyRole = "sub"; // 기본적으로 secondCompany는 sub으로 설정

    $(".dropbtn").click(function(){
        $(".dropdown-content").toggle();
    });

    $(".dropdown-content a").click(function(e){
        e.preventDefault(); // 기본 이벤트 방지
        selectedRelation = $(this).text(); // 선택한 관계 업데이트
        $(".dropbtn").text(selectedRelation); // 버튼 텍스트를 선택한 항목으로 변경
        $(".dropdown-content").hide(); // 드롭다운 메뉴 닫기
    });
    
    // 외부 클릭 시 드롭다운 메뉴 닫기
    $(document).click(function(e) {
        if (!$(e.target).closest('.dropdown').length) {
            $('.dropdown-content').hide();
        }
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
        } else {
            alert("적어도 하나의 필드를 채워주세요.");
        }
    });

    // 삭제 버튼에 대한 이벤트 위임 설정
    $("#companyTagContainer").on("click", ".delete-btn", function() {
        $(this).parent().remove(); // 해당 항목 삭제
    });
    ///////////////////////////////////////////////////////////////////////////
    

    ////////////////////////////// 대분류 중분류 //////////////////////////////
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

    // 1차 카테고리 모달 초기화
    createCategoryModal(primaryCategories, '#primaryCategoryModal', '#selectedPrimaryCategories', true);
    $('#openPrimaryModal').click(function() {
        $('#primaryCategoryModal').show();
    });

    // 2차 카테고리 모달 초기화
    createCategoryModal(secondaryCategories, '#secondaryCategoryModal', '#selectedSecondaryCategories', false);
    $('#openSecondaryModal').click(function() {
        $('#secondaryCategoryModal').show();
    });

    // 카테고리 모달 생성 함수
    function createCategoryModal(categories, modalId, selectedDivId, isSingleSelection) {
        var modal = $(modalId);
        $.each(categories, function(category, items) {
            var categoryDiv = $('<div>').addClass('category');
            $('<h3>').text(category).appendTo(categoryDiv);
            $.each(items, function(index, item) {
                $('<span>').addClass('category-item').text(item).click(function() {
                    // primary는 한 개만 선택되도록
                    if (isSingleSelection) {
                        $(modalId + ' .category-item').removeClass('selected');
                    }
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

    // 모달 닫기
    $('.close-modal').click(function() {
        $(this).closest('.modal').hide();
    });
    ///////////////////////////////////////////////////////////////////////////
});
