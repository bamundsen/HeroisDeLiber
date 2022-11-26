
  const optionsContent = document.querySelector("#options")
  optionsContent.addEventListener('click', choose, false)

  const option = {
    option: optionsContent.value
  }

  async function choose(e){
    var option = {
        option: e.target.value
    }
    
    const init = {
      method: "POST",
      headers: {
          'Content-type': 'application/json'
      },
      body: JSON.stringify(option)
    }

    const response = await fetch('/choose', init);
    const texts = await response.json();
    console.log(option);
    return texts;
  }

  async function loadcookie(){
    const response = await fetch('/loadcookies');
    const cookies = await response.json();
    console.log(cookies);
    return cookies;
  }
