function isWord(word) {
  if (/\s/g.test(word)) return false;
  if (/[-!$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/.test(word)) return false;
  if (/[0-9]/.test(word)) return false;
  
  return true;
}

document.addEventListener('DOMContentLoaded', async function() {
    document.querySelector('button').addEventListener('click' , async function() {
        let text = document.getElementById('text').value;
        if (text) {
            if (isWord(text)) {
                let url = `${urlCORS}https://www.stands4.com/services/v2/syno.php?uid=${UID}&tokenid=${tokenID}&word=${text}&format=json`
                let synonyms = [];
                let temp = [];
        
                const response = await fetch(url);
                const myJSON = await response.json();
            
                if (myJSON.result) {
                    const list = myJSON.result;
                
                    // treat when there is only one result
                    if (list.length > 0) {
                        list.forEach(element => {
                            synonyms.push(element.synonyms)
                        })
                    } else {
                        synonyms.push(list.synonyms);
                    }
        
                    synonyms.forEach(line => {
                        if (line.toString().indexOf(',') > -1) { temp = line.split(', ') }
                        })
                } else {
                    temp = 'No synonym found for this word';
                }

                alert = temp.toString().split(',');
                newText = alert.join(', ');

                if (newText.indexOf(',') >= 0) {
                    document.getElementById('result').innerHTML = `<div class="alert alert-success" role="alert">${newText}</div>`;
                } else {
                    document.getElementById('result').innerHTML = `<div class="alert alert-info" role="alert">${newText}</div>`;
                }
                
            } else {
                document.getElementById('result').innerHTML = `
                <div class="alert alert-warning" role="alert">
                    You must enter a word without special characters
                </div>`;
            }
        }
    });
});


