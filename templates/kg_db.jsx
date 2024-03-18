import React, { useState, useEffect } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [articleDate, setArticleDate] = useState('');
  const [article, setArticle] = useState('');
  const [selectedHighlight, setSelectedHighlight] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const highlight = localStorage.getItem('highlight') || '';
    setSelectedHighlight(highlight);
  }, []);

  const handleRadioChange = (event) => {
    const { name, id } = event.target;
    localStorage.setItem(name, id);
    setSelectedHighlight(id);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const formData = new FormData();
    formData.append('api_url', url);
    formData.append('api_title', title);
    formData.append('articleHighLight', article);
    // Adjust the URL and method according to your backend
    try {
      const response = await fetch('/load_content/kg_db', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      // Process your response data here
      console.log(data);
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    }
    setIsLoading(false);
  };

  return (
    <div className="total">
      <div className="box-top">
        <h3>- Knowledge Graph Training Data -</h3>
      </div>
      <div className="box-wrap-upper">
        <form onSubmit={handleSubmit} id="inputForm">
          <div className="box1">
            <p>
              기사 주소 (URL) :<br />
              <input type="text" name="api_url" size="99" placeholder="연합 뉴스 혹은 이투데이 기사 주소를 넣어주세요." value={url} onChange={(e) => setUrl(e.target.value)} /><br />
              <input type="submit" className="sub_button" id="url_button" value="URL 기사 검색" />
            </p>
            <p>
              제목 : <br />
              <input type="text" id="title_text" name="api_title" size="99" placeholder="제목." value={title} onChange={(e) => setTitle(e.target.value)} />
            </p>
            <p>
              기사 : (기사 송고 시간 : {articleDate})<br />
              <div contentEditable="true" className="editable-div" id="editableDiv" onBlur={(e) => setArticle(e.target.innerHTML)} dangerouslySetInnerHTML={{ __html: article }}></div>
            </p>
            <p>
              <input type="submit" className="sub_button" value="데이터 생성" />
              {isLoading && <p>Loading...</p>}
            </p>
          </div>
        </form>
        {/* Other parts of the form */}
      </div>
    </div>
  );
}

export default App;
