$(document).ready(function() {
    // 불렛의 실시간 글자 수 계산 및 전체 글자 수 업데이트 함수
    function updateTotalCharCount() {
        let totalCharCount = 0;

        // 모든 불렛의 글자 수 합산
        $('.bullet').each(function() {
            totalCharCount += $(this).text().length;
        });

        // 합산한 글자 수를 총 글자 수 div에 표시
        $('#total-char-count').text(`총 글자 수: ${totalCharCount}`);
    }

    let sectionCount = 0;  // 중제 카운트
    let bulletCount = 1;   // 불렛 카운트

    // 중제 추가 함수
    function addSection() {
        sectionCount++; // 고유한 ID 생성을 위한 숫자 증가
        bulletCount = 1; // 각 중제마다 불렛 카운트 초기화
        let referenceCount = { 1: 1 }; // 각 불렛마다 별도로 관리되는 참고 문서 수

        // 중제 섹션 HTML 생성
        var newSection = `
            <div class="section" id="section-${sectionCount}" data-section-id="${sectionCount}">
                <div class="flex-container">
                    <div class="sign"><b>중제 ${sectionCount}</b></div>
                    <div contenteditable="true" class="subtitle" id="subtitle-${sectionCount}"></div>
                    <button class="delete-btn delete-section" data-section-id="${sectionCount}">삭제</button>
                </div>
                <!-- 기본적으로 불렛과 참고 문서가 하나씩 생성됨 -->
                <div class="bullet-section" id="bullet-section-${sectionCount}-1" data-bullet-id="1">
                    <div class="flex-container">
                        <div class="sign bullet-sign"><b>불렛 1</b></div>
                        <div contenteditable="true" class="bullet" id="bullet-${sectionCount}-1"></div>
                        <button class="delete-btn delete-bullet" data-section-id="${sectionCount}" data-bullet-id="1">삭제</button>
                    </div>
                    <!-- 글자 수 표시를 위한 영역 추가 -->
                    <div class="char-count" id="char-count-${sectionCount}-1">글자 수: 0</div>
                    <div class="reference-section" id="reference-section-${sectionCount}-1-1" data-reference-id="1">
                        <div class="flex-container">
                            <div class="sign"><b>참고 문서</b></div>
                            <div contenteditable="true" class="reference" id="reference-${sectionCount}-1-1"></div>
                            <button class="delete-btn delete-reference" data-section-id="${sectionCount}" data-bullet-id="1" data-reference-id="1">삭제</button>
                        </div>
                    </div>
                    <!-- 참고 문서 추가 버튼 -->
                    <button class="add-ref" data-section-id="${sectionCount}" data-bullet-id="1">참고 문서 추가</button>
                </div>
                <!-- 불렛 추가 버튼 -->
                <button class="add-bullet" data-section-id="${sectionCount}">불렛 추가</button>
            </div>
        `;

        // 새로운 섹션을 기존 구조 끝에 추가
        $(newSection).insertBefore('#subTitleButton');

        // 불렛의 실시간 글자 수 계산
        $(`#bullet-${sectionCount}-1`).on('keyup', function() {
            let charCount = $(this).text().length;
            $(`#char-count-${sectionCount}-1`).text(`글자 수: ${charCount}`);
            // 총 글자 수 업데이트
            updateTotalCharCount();
        });
    }


    // 불렛 추가 함수
    function addBullet(sectionId, bulletCount) {
        let referenceCount = 1;

        var newBullet = `
            <div class="bullet-section" id="bullet-section-${sectionId}-${bulletCount}" data-bullet-id="${bulletCount}">
                <div class="flex-container">
                    <div class="sign bullet-sign"><b>불렛 ${bulletCount}</b></div>
                    <div contenteditable="true" class="bullet" id="bullet-${sectionId}-${bulletCount}"></div>
                    <button class="delete-btn delete-bullet" data-section-id="${sectionId}" data-bullet-id="${bulletCount}">삭제</button>
                </div>
                <!-- 글자 수 표시를 위한 영역 추가 -->
                <div class="char-count" id="char-count-${sectionId}-${bulletCount}">글자 수: 0</div>
                <div class="reference-section" id="reference-section-${sectionId}-${bulletCount}-1" data-reference-id="1">
                    <div class="flex-container">
                        <div class="sign"><b>참고 문서</b></div>
                        <div contenteditable="true" class="reference" id="reference-${sectionId}-${bulletCount}-1"></div>
                        <button class="delete-btn delete-reference" data-section-id="${sectionId}" data-bullet-id="${bulletCount}" data-reference-id="1">삭제</button>
                    </div>
                </div>
                <button class="add-ref" data-section-id="${sectionId}" data-bullet-id="${bulletCount}">참고 문서 추가</button>
            </div>
        `;
        // 새로운 불렛을 기존 구조 끝에 추가
        $(`#section-${sectionId} .add-bullet`).before(newBullet);

        // 실시간 글자 수 업데이트
        $(`#bullet-${sectionId}-${bulletCount}`).on('keyup', function() {
            let charCount = $(this).text().length;
            $(`#char-count-${sectionId}-${bulletCount}`).text(`글자 수: ${charCount}`);
            // 총 글자 수 업데이트
            updateTotalCharCount();
        });
    }
    

    // 참고 문서 추가 함수
    function addReference(sectionId, bulletId, referenceCount) {
        var newReference = `
            <div class="reference-section" id="reference-section-${sectionId}-${bulletId}-${referenceCount}" data-reference-id="${referenceCount}">
                <div class="flex-container">
                    <div class="sign"><b>참고 문서</b></div>
                    <div contenteditable="true" class="reference" id="reference-${sectionId}-${bulletId}-${referenceCount}"></div>
                    <button class="delete-btn delete-reference" data-section-id="${sectionId}" data-bullet-id="${bulletId}" data-reference-id="${referenceCount}">삭제</button>
                </div>
            </div>
        `;
        $(`#bullet-section-${sectionId}-${bulletId} .add-ref`).before(newReference);
    }


    // 불렛 삭제 시에도 총 글자 수 업데이트
    $(document).on('click', '.delete-bullet', function() {
        const sectionId = $(this).data('section-id');
        const bulletId = $(this).data('bullet-id');
        $(`#bullet-section-${sectionId}-${bulletId}`).remove();

        // 총 글자 수 업데이트
        updateTotalCharCount();
    });

    // 중제 삭제 시에도 총 글자 수 업데이트
    $(document).on('click', '.delete-section', function() {
        const sectionId = $(this).data('section-id');
        $(`#section-${sectionId}`).remove();

        // 총 글자 수 업데이트
        updateTotalCharCount();
    });

    // 페이지가 로드될 때 기본 중제를 추가
    $(document).ready(function() {
        addSection();
    });
    
    // 페이지 로드 시 subTitleButton 클릭
    $('#subTitleButton').click(addSection);

    // 저장 버튼 클릭 이벤트
    $('#saveButton').click(function() {
        // 글 제목과 핵심 데이터를 처리
        let title = cleanText($('#titleDiv').html());
        let core = cleanText($('#coreDiv').html());

        // 중제, 불렛, 참고 문서 데이터를 수집
        let article = {};  // 각 중제와 그 안의 불렛, 참고 문서를 담을 객체

        // 각 중제 섹션을 순회하며 데이터를 수집
        $('.section').each(function(sectionIndex) {
            let sectionId = $(this).data('section-id');
            appendSectionData(sectionId, article);
        });

        // 서버로 전송할 전체 데이터를 JSON 객체로 생성
        let dataToSend = {
            title: title,
            core: core,
            article: [article]  // article을 리스트로 감싸서 보냄
        };

        // 서버로 JSON 데이터를 전송
        $.ajax({
            url: '/utile/reference_api',  // 데이터를 전송할 API URL
            type: 'POST',
            contentType: 'application/json',  // JSON 형식으로 전송
            data: JSON.stringify(dataToSend),  // 데이터를 JSON 문자열로 변환
            success: function(response) {
                // 응답의 'code' 값 확인
                if (response.code === 'SUCCESS') {
                    alert('저장이 완료되었습니다.');
                    
                    // 텍스트 필드 초기화
                    $('#titleDiv').html('');
                    $('#coreDiv').html('');

                    // 동적으로 추가된 중제와 불렛 섹션들 삭제
                    $('.section').remove();
                    
                    // 카운터 초기화
                    sectionCount = 0;
                    bulletCount = 1;
                    
                    // 기본 중제 추가 버튼 클릭하여 처음 상태로 되돌림
                    $('#subTitleButton').click();
                } else if (response.code === 'ERROR') {
                    alert('저장에 실패했습니다.');
                } else {
                    alert('예기치 못한 응답을 받았습니다.');
                }
            },
            error: function(error) {
                alert('저장에 실패했습니다.');
            }
        });
    });


    // 불렛 추가 버튼 클릭 이벤트
    $(document).on('click', '.add-bullet', function() {
        let sectionId = $(this).data('section-id');
        bulletCount++; // 해당 중제에서만 증가하는 불렛 카운트
        addBullet(sectionId, bulletCount);
    });

    // 참고 문서 추가 버튼 클릭 이벤트
    $(document).on('click', '.add-ref', function() {
        let sectionId = $(this).data('section-id');
        let bulletId = $(this).data('bullet-id');
        let referenceCount = $(`#bullet-section-${sectionId}-${bulletId} .reference-section`).length + 1;
        addReference(sectionId, bulletId, referenceCount);
    });

    // 중제 삭제 버튼 클릭 이벤트
    $(document).on('click', '.delete-section', function() {
        const sectionId = $(this).data('section-id');
        $(`#section-${sectionId}`).remove();
    });

    // 불렛 삭제 버튼 클릭 이벤트
    $(document).on('click', '.delete-bullet', function() {
        const sectionId = $(this).data('section-id');
        const bulletId = $(this).data('bullet-id');
        $(`#bullet-section-${sectionId}-${bulletId}`).remove();
    });

    // 참고 문서 삭제 버튼 클릭 이벤트
    $(document).on('click', '.delete-reference', function() {
        const sectionId = $(this).data('section-id');
        const bulletId = $(this).data('bullet-id');
        const referenceId = $(this).data('reference-id');
        $(`#reference-section-${sectionId}-${bulletId}-${referenceId}`).remove();
    });

    // 줄바꿈 방지: 중제와 참고 문서에서 엔터키 비활성화
    $(document).on('keydown', '.subtitle, .reference', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // 엔터키 동작을 막음
        }
    });

    // 텍스트 필드를 깨끗하게 처리하는 함수
    function cleanText(html) {
        return (html || '')
            .replace(/<div>/gi, '\n')         // <div> 태그를 줄바꿈으로 변환
            .replace(/<\/?[^>]+(>|$)/g, '') // 모든 HTML 태그 제거
            .replace(/\r\n/g, '\n')         // 줄바꿈 통일
            .replace(/&nbsp;/g, ' ')        // &nbsp;를 일반 공백으로 변환
            .trim();
    }

    // 각 contenteditable 요소의 데이터를 JSON 객체에 추가하는 함수
    function appendSectionData(sectionId, article) {
        let sectionTitle = cleanText($(`#subtitle-${sectionId}`).html());
        let sectionData = { sectionTitle };

        // 불렛 데이터를 수집
        $(`#section-${sectionId} .bullet-section`).each(function(bulletIndex) {
            let bulletId = $(this).data('bullet-id');
            let bulletText = cleanText($(`#bullet-${sectionId}-${bulletId}`).html());
            let bulletData = { bulletText };

            // 참고 문서 데이터를 수집
            $(`#bullet-section-${sectionId}-${bulletId} .reference-section`).each(function(referenceIndex) {
                let referenceId = $(this).data('reference-id');
                let referenceText = cleanText($(`#reference-${sectionId}-${bulletId}-${referenceId}`).html());
                bulletData[`reference${referenceIndex + 1}`] = referenceText;
            });

            sectionData[`bullet${bulletIndex + 1}`] = bulletData;
        });

        article[`section${sectionId}`] = sectionData;
    }

    $('#copyButton').click(function() {
        // 글 제목과 핵심 데이터를 처리
        // let title = cleanText($('#titleDiv').html() || '');
        let core = cleanText($('#coreDiv').html() || '');
    
        // 중간 제목과 불렛 텍스트를 수집할 변수
        let articleText = '';
    
        // 각 중간 제목과 불렛을 순회하면서 데이터를 수집
        $('.section').each(function() {
            let sectionId = $(this).data('section-id');
            let sectionTitle = cleanText($(`#subtitle-${sectionId}`).html() || '');
    
            if (sectionTitle) { // 중간 제목이 있을 경우에만 추가
                articleText += `${sectionTitle}\n`;
            }
    
            // 해당 중제 내 불렛들을 순회하며 데이터 수집
            $(`#section-${sectionId} .bullet-section`).each(function() {
                let bulletId = $(this).data('bullet-id');
                let bulletText = cleanText($(`#bullet-${sectionId}-${bulletId}`).html() || '');
    
                if (bulletText) { // 불렛이 있을 경우에만 추가
                    articleText += `${bulletText}\n`;
                }
            });
        });
    
        // 최종 텍스트 복사
        // let textToCopy = `${title}\n${core}\n${articleText}`.trim();
        let textToCopy = `${core}\n${articleText}`.trim();
    
        navigator.clipboard.writeText(textToCopy).then(function() {
            alert('내용이 클립보드에 복사되었습니다.');
        }, function(err) {
            alert('복사에 실패했습니다: ' + err);
        });
    });
});
