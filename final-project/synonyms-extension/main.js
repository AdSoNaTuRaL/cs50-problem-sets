function isWord(word) {
  if (/\s/g.test(word)) return false;
  if (/[-!$%^&*()_+|~=`{}\[\]:";'<>?,.\/]/.test(word)) return false;
  if (/[0-9]/.test(word)) return false;

  return true;
}

async function getEnSynonyms(word) {
  const url = `${urlCORS}https://www.stands4.com/services/v2/syno.php?uid=${UID}&tokenid=${tokenID}&word=${word}&format=json`;

  let synonyms = [];
  let temp = [];

  const response = await fetch(url);
  const myJSON = await response.json();

  if (myJSON.result) {
    const list = myJSON.result;

    // treat when there is only one result
    if (list.length > 0) {
      list.forEach((element) => {
        synonyms.push(element.synonyms);
      });
    } else {
      synonyms.push(list.synonyms);
    }

    synonyms.forEach((line) => {
      if (line.toString().indexOf(",") > -1) {
        temp = line.split(", ");
      }
    });
  } else {
    temp = "No synonym found for this word";
  }

  return temp;
}

async function getptBRSynonyms(word) {
  const url = `https://synonyms-ptbr.herokuapp.com/synonym?q=${word}`;

  let synonyms = [];

  const response = await fetch(url);
  const myJSON = await response.json();

  if (myJSON.synonyms) {
    const list = myJSON.synonyms;

    list.forEach((element) => {
      synonyms.push(element);
    });
  } else {
    synonyms = "Nenhum sinônimo encontrado para esta palavra";
  }

  return synonyms;
}

document.addEventListener("DOMContentLoaded", async function () {
  var userLang = navigator.language || navigator.userLanguage;

  userLang === "pt-BR"
    ? (document.getElementById("checkLanguage").checked = true)
    : (document.getElementById("checkLanguage").checked = false);

  document.querySelector("button").addEventListener("click", async function () {
    let word = document.getElementById("word").value;

    if ($("#checkLanguage").is(":checked")) {
      if (word) {
        if (isWord(word)) {
          let result = await getptBRSynonyms(word);

          if (result.length === 0) {
            document.getElementById("result").innerHTML = `
              <div class="alert alert-info" role="alert">
                Nenhum sinônimo encontrado para esta palavra
              </div>`;
            return;
          }

          alert = result.toString().split(",");
          newText = alert.join(", ");

          if (newText.indexOf(",") >= 0) {
            document.getElementById(
              "result"
            ).innerHTML = `<div class="alert alert-success" role="alert">${newText}</div>`;
          } else {
            document.getElementById(
              "result"
            ).innerHTML = `<div class="alert alert-info" role="alert">${newText}</div>`;
          }
        } else {
          document.getElementById("result").innerHTML = `
            <div class="alert alert-warning" role="alert">
                Você deve inserir uma palavra sem caracteres especiais
            </div>
            `;
        }
      } else {
        document.getElementById("word").style.border = `
        1px solid #ff0000 
        `;
      }
    } else {
      if (word) {
        if (isWord(word)) {
          let result = await getEnSynonyms(word);
          alert = result.toString().split(",");
          newText = alert.join(", ");

          if (newText.indexOf(",") >= 0) {
            document.getElementById(
              "result"
            ).innerHTML = `<div class="alert alert-success" role="alert">${newText}</div>`;
          } else {
            document.getElementById(
              "result"
            ).innerHTML = `<div class="alert alert-info" role="alert">${newText}</div>`;
          }
        } else {
          document.getElementById("result").innerHTML = `
            <div class="alert alert-warning" role="alert">
                You must enter a word without special characters
            </div>`;
        }
      } else {
        document.getElementById("word").style.border = `
        1px solid #ff0000 
        `;
      }
    }
  });
});
