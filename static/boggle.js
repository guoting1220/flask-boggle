$(async function(){
  const $guessWord = $("#word");
  const $guessForm = $("#guess-form");
  const $result = $("#result");
  const $score = $("#score");
  const $startBtn = $("#start-btn");
  const $scoreInfo = $("#score-info");
  const $timer = $("#timer");
  const $timeUp = $("#time-up");
  const $timerSec = $("#timer-sec");
  const $highest = $("#highest-score");
  const $playTimes = $("#play-times");

  let wordList = [];
  let score = 0;


  /* add event listener on start button =========================== */

  $startBtn.on("click", function() {
    resetGame();
  })

  /* handle the submit of the guess word form ===================== */

  $guessForm.on("submit", async function (e) {
    e.preventDefault();
    displayElements("show", [$result]);
    let guessWord = $guessWord.val();

    // take the form value and using axios, make an AJAX request to send it to the server.
    const res = await axios.get("/check-word", {params: {"word": guessWord}});

    if (res.data.result === "ok") {
      if (wordList.indexOf(guessWord) !== -1) {
        $result.text("You already submitted this word!");
        toggleStyle($result, "fail");
        toggleStyle($result, "success");
      }
      else {
        $result.text("Great!");
        toggleStyle($result, "fail", "success");
        score += guessWord.length;
        wordList.push(guessWord);
      }
    }
    else {
      if (res.data.result === "not-on-board") {
        $result.text("Sorry! The word is not on the board!");
      }
      else {
        $result.text("Sorry! It is not a word!");
      }

      toggleStyle($result, "success", "fail");
    }

    $score.text(score);
    $guessWord.val("").focus();
  });



  /* start or reset the game ======================================*/

  function resetGame() {
    wordList = [];
    score = 0;
    displayElements("hide", [$startBtn, $timeUp]);
    displayElements("show", [$timer, $scoreInfo, $guessForm]);
    $score.text(score);
    $guessWord.val("").focus();
    setTimer();
  }

  /* set timer when starting the game ============================= */

  function setTimer(totalSecs = 10) {
    $timerSec.text(totalSecs);  //60
    let count = totalSecs - 1;  // 59
    let timer = setInterval(async function () {
      $timerSec.text(count--);
      if (count === 0) {
        clearInterval(timer);
        handleTimeUp();
      }
    }, 1000);
  }

  /* send info to server when game is over, 
  get response and uodate the page ===============================*/

  async function handleTimeUp(){
    displayElements("hide", [$timer, $guessForm, $result]);
    displayElements("show", [$startBtn, $timeUp]);
    $startBtn.text("Restart")

    // When the game ends, send an AJAX request to the server with the score you have stored on the front-end and increment the number of times you have played on the backend.
    const res = await axios.post("/post-score", {"score": score});
    $highest.text(res.data.highest_score);
    $playTimes.text(res.data.times_of_plays);
  }

  /* change the style of the element from one to another ========  */
  function toggleStyle($ele, fromStyle, toStyle="") {    
    $ele.addClass(toStyle);
    $ele.removeClass(fromStyle);
  }

  /* show or hide elements in elementsArr =========================*/

  function displayElements(dispayType, elementsArr) {
    if (dispayType === "show") {
      elementsArr.forEach($elem => $elem.show());
    }
    else if (dispayType === "hide") {
      elementsArr.forEach($elem => $elem.hide());
    }
  }

});