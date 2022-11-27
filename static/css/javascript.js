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
    const content = await response.json();
    console.log(content);
    document.getElementById("consequenceText").innerHTML = content['consequence'];

    //textos da próxima escolha
    document.getElementById("act_name").innerHTML = content['event_content']['act_name'];
    document.getElementById("icon").src = content['event_content']['icon'];
    document.getElementById("lore").innerHTML = content['event_content']['lore'];
    var options = document.getElementById("options");
    var picks = options.children;
    for (var i=0; i < content['event_content']['options'].length; i++){
      var pick = picks[i];
      pick.innerHTML = content['event_content']['options'][i];
    }

    return content;
  }

  window.onload = async function loadcookie(){
    const response = await fetch('/loadcookies');
    const content = await response.json();
    console.log(content);
    document.getElementById("act_name").innerHTML = content['event_content']['act_name'];
    document.getElementById("icon").src = content['event_content']['icon'];
    document.getElementById("lore").innerHTML = content['event_content']['lore'];
    var options = document.getElementById("options");
    var picks = options.children;
    for (var i=0; i < content['event_content']['options'].length; i++){
      var pick = picks[i];
      pick.innerHTML = content['event_content']['options'][i];
    }

    return content;
  }
