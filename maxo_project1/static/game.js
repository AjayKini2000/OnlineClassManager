const question = document.getElementById("question");
const choices = Array.from(document.getElementsByClassName("choice-text"));
const progressText = document.getElementById("qst");

let currentQuestion = {};
let acceptingAnswers = false;
let score = 0;
let questionCounter = 0;
let availableQuesions = [];


let questions = [
  {
    question: "Which state produces maximum soybean?",
    choice1: " Madhya Pradesh",
    choice2: "Uttar Pradesh",
    choice3: "Bihar",
    choice4: "Rajasthan",
    answer: 1
  },
  {
    question:
      "Which country operationalized world’s largest radio telescope?",
    choice1: "USA",
    choice2: "China",
    choice3: "Russia",
    choice4: "India",
    answer: 2
  },
  {
    question:
      "Which of the following is the capital of Arunachal Pradesh?",
    choice1: "Itanagar",
    choice2: "Dispur",
    choice3: "Imphal",
    choice4: "Panaji",
    answer: 1
  },
  {
    question:
      "Katerina Sakellaropoulou was elected the first woman President of",
    choice1: "Greece",
    choice2: "Spain",
    choice3: "Finland",
    choice4: "Netherland",
    answer: 1
  },
  {
    question:
      "Which one among the following radiations carries maximum energy?",
    choice1: "Ultraviolet rays",
    choice2: "Gamma rays",
    choice3: "X- rays",
    choice4: "Infra-red rays",
    answer: 2
  },
  {
    question:
      "What is India’s rank on EIU’s Global Democracy Index 2019?",
    choice1: "48th Rank",
    choice2: "50th Rank",
    choice3: "53th Rank",
    choice4: "51th Rank",
    answer: 4
  },
  {
    question:
      "Which of the following states is not located in the North?",
    choice1: "Jharkhand",
    choice2: "Jammu and Kashmir",
    choice3: "Himachal Pradesh",
    choice4: "Haryana",
    answer: 1
  },
  {
    question:
      "What is India’s rank on the WEF’s Global Social Mobility Index 2020?",
    choice1: "75th Rank",
    choice2: "77th Rank",
    choice3: "76th Rank",
    choice4: "78th Rank",
    answer: 3
  },
  {
    question:
      "Bokaro Steel Limited was established with the assistance of",
    choice1: "Germany",
    choice2: "Soviet Union",
    choice3: "UK",
    choice4: "USA",
    answer: 2
  },
  {
    question: "Which is the largest coffee producing state of India?",
    choice1: "Kerala",
    choice2: "Tamil Nadu",
    choice3: "Karnataka",
    choice4: "Arunachal Pradesh",
    answer: 3
  }
];

//CONSTANTS
const CORRECT_BONUS = 10;
const MAX_QUESTIONS = 10;

startGame = () => {
  questionCounter = 0;
  score = 0;
  availableQuesions = [...questions];
  getNewQuestion();
};

getNewQuestion = () => {
  if (availableQuesions.length === 0 || questionCounter >= MAX_QUESTIONS) {
    localStorage.setItem("mostRecentScore", score);
    localStorage.setItem("RecentScore", score);
    //go to the end page
    return window.location.assign("http://127.0.0.1:5000/end");
  }
  questionCounter++;
  progressText.innerText = `Question ${questionCounter}/${MAX_QUESTIONS}`;
  const questionIndex = Math.floor(Math.random() * availableQuesions.length);
  currentQuestion = availableQuesions[questionIndex];
  question.innerText = currentQuestion.question;

  choices.forEach(choice => {
    const number = choice.dataset["number"];
    choice.innerText = currentQuestion["choice" + number];
  });

  availableQuesions.splice(questionIndex, 1);
  acceptingAnswers = true;
};

choices.forEach(choice => {
  choice.addEventListener("click", e => {
    if (!acceptingAnswers) return;

    acceptingAnswers = false;
    const selectedChoice = e.target;
    const selectedAnswer = selectedChoice.dataset["number"];

    const classToApply =
      selectedAnswer == currentQuestion.answer ? "correct" : "incorrect";
      
      if (classToApply === "correct") {
        incrementScore(CORRECT_BONUS);
      }
      // window.location.assign("balloon.html");

    selectedChoice.classList.add(classToApply);
    
    setTimeout(() => {
      selectedChoice.classList.remove(classToApply);
      getNewQuestion();
    }, 1000);
  });
});

incrementScore = num => {
  score += num;
  
};

startGame();
