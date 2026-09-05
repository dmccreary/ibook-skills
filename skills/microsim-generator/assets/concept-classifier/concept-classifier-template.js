// Concept Classifier Quiz MicroSim Template
// A generalized classification quiz where students identify categories from scenarios
// Customize: Replace $QUIZ_TITLE, $QUIZ_DESCRIPTION, and mascot as needed

// Canvas dimensions
let canvasWidth = 800;
let drawHeight = 480;
let controlHeight = 50;
let canvasHeight = drawHeight + controlHeight;
let margin = 20;
let defaultTextSize = 16;

// Quiz state
let quizData = null;
let scenarios = [];
let currentScenarioIndex = 0;
let score = 0;
let answered = false;
let selectedAnswer = -1;
let usedHint = false;
let quizComplete = false;

// Configuration (loaded from data.json or defaults)
let config = {
  questionsPerQuiz: 10,
  pointsCorrect: 10,
  pointsWithHint: 5,
  scenarioLabel: 'SCENARIO',
  instructionText: 'Select the correct classification',
  correctAnswerField: 'correctAnswer'
};

// Animation states
let feedbackAlpha = 0;
let feedbackColor = [0, 200, 0];
let feedbackMessage = '';

// UI elements
let nextButton;
let hintButton;
let restartButton;

// Mascot character states
let mascotExpression = 'neutral'; // neutral, happy, thinking

// Option buttons (virtual)
let optionButtons = [];

async function setup() {
  updateCanvasSize();
  const canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));

  // Load quiz data from JSON file
  quizData = await loadJSON('data.json');

  // Load configuration if present
  if (quizData && quizData.config) {
    Object.assign(config, quizData.config);
  }

  // Initialize scenarios from loaded data (select random questions)
  if (quizData && quizData.scenarios) {
    let shuffled = shuffle([...quizData.scenarios]);
    scenarios = shuffled.slice(0, config.questionsPerQuiz);
  }

  // Create control buttons
  hintButton = createButton('Show Hint');
  hintButton.mousePressed(showHint);

  nextButton = createButton('Next');
  nextButton.mousePressed(nextScenario);
  nextButton.hide();

  restartButton = createButton('Restart Quiz');
  restartButton.mousePressed(restartQuiz);
  restartButton.hide();

  positionButtons();

  // Accessibility description
  let title = quizData?.title || 'Concept Classifier Quiz';
  describe(title + ' - an interactive classification quiz', LABEL);
}

function positionButtons() {
  let buttonY = drawHeight + 12;
  hintButton.position(margin, buttonY);
  nextButton.position(margin + 100, buttonY);
  restartButton.position(margin, buttonY);
}

function draw() {
  updateCanvasSize();

  // Drawing area background
  fill('aliceblue');
  stroke('silver');
  strokeWeight(1);
  rect(0, 0, canvasWidth, drawHeight);

  // Control area background
  fill('white');
  noStroke();
  rect(0, drawHeight, canvasWidth, controlHeight);

  if (!quizData || !quizData.scenarios) {
    fill(0);
    textSize(20);
    textAlign(CENTER, CENTER);
    text('Loading quiz data...', canvasWidth/2, drawHeight/2);
    return;
  }

  if (quizComplete) {
    drawEndScreen();
  } else {
    drawQuizScreen();
  }

  // Update feedback animation
  if (feedbackAlpha > 0) {
    feedbackAlpha -= 5;
  }
}

function drawQuizScreen() {
  let currentScenario = scenarios[currentScenarioIndex];

  // Title
  fill(30, 60, 90);
  noStroke();
  textSize(22);
  textAlign(CENTER, TOP);
  textStyle(BOLD);
  let title = quizData?.title || 'Concept Classifier Quiz';
  text(title, canvasWidth * 0.4, 12);
  textStyle(NORMAL);

  // Score and progress display (top right)
  drawScorePanel();

  // Draw mascot character
  drawMascotCharacter(canvasWidth - 80, 120);

  // Scenario card
  drawScenarioCard(currentScenario);

  // Option buttons
  drawOptionButtons(currentScenario);

  // Feedback flash
  if (feedbackAlpha > 0) {
    noStroke();
    fill(feedbackColor[0], feedbackColor[1], feedbackColor[2], feedbackAlpha);
    rect(0, 0, canvasWidth, drawHeight);
  }

  // Explanation panel (always show after answering)
  if (answered) {
    drawExplanationPanel(currentScenario);
  }

  // Hint panel
  if (usedHint && !answered) {
    drawHintPanel(currentScenario);
  }

  // Control area labels
  fill(60);
  textSize(14);
  textAlign(CENTER, CENTER);
  if (!answered) {
    text(config.instructionText, canvasWidth * 0.6, drawHeight + 25);
  } else {
    text('Review the explanation, then continue', canvasWidth - 280, drawHeight + 25);
  }
}

function drawScorePanel() {
  let panelX = canvasWidth - 150;
  let panelY = 10;
  let panelW = 140;
  let panelH = 70;

  // Panel background
  fill(255, 255, 255, 230);
  stroke(200);
  strokeWeight(1);
  rect(panelX, panelY, panelW, panelH, 10);

  // Score
  fill(30, 100, 60);
  noStroke();
  textSize(14);
  textAlign(LEFT, TOP);
  text('Score:', panelX + 10, panelY + 10);
  textSize(24);
  textStyle(BOLD);
  text(score, panelX + 70, panelY + 5);
  textStyle(NORMAL);

  // Progress
  fill(60);
  textSize(14);
  text('Progress:', panelX + 10, panelY + 40);
  textSize(16);
  text((currentScenarioIndex + 1) + ' / ' + scenarios.length, panelX + 80, panelY + 38);

  // Progress bar
  let barX = panelX + 10;
  let barY = panelY + 58;
  let barW = panelW - 20;
  let barH = 6;
  fill(220);
  noStroke();
  rect(barX, barY, barW, barH, 3);
  fill(70, 130, 180);
  let progress = (currentScenarioIndex + 1) / scenarios.length;
  rect(barX, barY, barW * progress, barH, 3);
}

function drawScenarioCard(scenario) {
  let cardX = margin;
  let cardY = 50;
  let cardW = canvasWidth - 180;
  let cardH = 140;

  // Card shadow
  fill(0, 0, 0, 30);
  noStroke();
  rect(cardX + 4, cardY + 4, cardW, cardH, 10);

  // Card background
  fill(255);
  stroke(100, 140, 180);
  strokeWeight(2);
  rect(cardX, cardY, cardW, cardH, 10);

  // Scenario label
  fill(70, 130, 180);
  noStroke();
  textSize(12);
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  text(config.scenarioLabel + ' ' + (currentScenarioIndex + 1), cardX + 15, cardY + 12);
  textStyle(NORMAL);

  // Scenario text
  fill(40);
  textSize(16);
  textAlign(LEFT, TOP);
  textWrap(WORD);
  text(scenario.scenario, cardX + 15, cardY + 35, cardW - 30, cardH - 50);
}

function drawOptionButtons(scenario) {
  let startY = 210;
  let buttonW = (canvasWidth - 180) / 2 - 15;
  let buttonH = 50;
  let gap = 10;

  optionButtons = [];
  let correctField = config.correctAnswerField;
  let correctAnswer = scenario[correctField];

  for (let i = 0; i < scenario.options.length; i++) {
    let col = i % 2;
    let row = floor(i / 2);
    let bx = margin + col * (buttonW + gap);
    let by = startY + row * (buttonH + gap);

    optionButtons.push({x: bx, y: by, w: buttonW, h: buttonH, index: i});

    // Determine button color
    let bgColor, textColor, borderColor;

    if (answered) {
      if (scenario.options[i] === correctAnswer) {
        bgColor = color(200, 240, 200);
        borderColor = color(60, 150, 60);
        textColor = color(30, 80, 30);
      } else if (i === selectedAnswer) {
        bgColor = color(255, 220, 200);
        borderColor = color(200, 100, 80);
        textColor = color(120, 50, 30);
      } else {
        bgColor = color(240);
        borderColor = color(180);
        textColor = color(120);
      }
    } else {
      let isHover = mouseX > bx && mouseX < bx + buttonW &&
                    mouseY > by && mouseY < by + buttonH;
      if (isHover) {
        bgColor = color(230, 240, 250);
        borderColor = color(70, 130, 180);
        textColor = color(40, 80, 120);
      } else {
        bgColor = color(250);
        borderColor = color(180);
        textColor = color(60);
      }
    }

    // Draw button
    fill(bgColor);
    stroke(borderColor);
    strokeWeight(2);
    rect(bx, by, buttonW, buttonH, 8);

    // Button text
    fill(textColor);
    noStroke();
    textSize(15);
    textAlign(CENTER, CENTER);
    textStyle(BOLD);
    text(scenario.options[i], bx + buttonW/2, by + buttonH/2);
    textStyle(NORMAL);

    // Checkmark or X for answered
    if (answered) {
      textSize(20);
      if (scenario.options[i] === correctAnswer) {
        fill(60, 150, 60);
        text('✓', bx + buttonW - 20, by + buttonH/2);
      } else if (i === selectedAnswer) {
        fill(200, 80, 60);
        text('✗', bx + buttonW - 20, by + buttonH/2);
      }
    }
  }

  // Feedback message
  if (answered && feedbackMessage) {
    let msgY = startY + 120;
    let isCorrect = scenario.options[selectedAnswer] === correctAnswer;

    fill(isCorrect ? color(40, 120, 60) : color(180, 100, 60));
    textSize(18);
    textAlign(CENTER, TOP);
    textStyle(BOLD);
    text(feedbackMessage, (canvasWidth - 180) / 2 + margin, msgY);
    textStyle(NORMAL);
  }
}

function drawExplanationPanel(scenario) {
  let panelX = margin;
  let panelY = 360;
  let panelW = canvasWidth - 180;
  let panelH = 100;

  // Panel background
  fill(255, 250, 240);
  stroke(200, 180, 140);
  strokeWeight(1);
  rect(panelX, panelY, panelW, panelH, 10);

  // Title
  fill(140, 100, 40);
  noStroke();
  textSize(14);
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  text('EXPLANATION', panelX + 12, panelY + 10);
  textStyle(NORMAL);

  // Explanation text
  fill(80, 60, 30);
  textSize(14);
  textWrap(WORD);
  text(scenario.explanation, panelX + 12, panelY + 30, panelW - 24, panelH - 40);
}

function drawHintPanel(scenario) {
  let panelX = margin;
  let panelY = 340;
  let panelW = canvasWidth - 180;
  let panelH = 60;

  // Panel background
  fill(255, 255, 230);
  stroke(200, 200, 140);
  strokeWeight(1);
  rect(panelX, panelY, panelW, panelH, 10);

  // Hint label
  fill(180, 160, 40);
  noStroke();
  textSize(14);
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  text('HINT', panelX + 12, panelY + 10);
  textStyle(NORMAL);

  // Hint text
  fill(100, 90, 40);
  textSize(14);
  text(scenario.hint, panelX + 12, panelY + 32);
}

// Mascot character - customize this function for different themes
function drawMascotCharacter(x, y) {
  // Default: Brain character
  // Replace this function to use a different mascot

  // Brain body
  fill(255, 200, 200);
  stroke(200, 150, 150);
  strokeWeight(2);

  // Main brain shape (simplified)
  ellipse(x, y, 60, 50);
  ellipse(x - 15, y - 10, 30, 25);
  ellipse(x + 15, y - 10, 30, 25);
  ellipse(x - 10, y + 10, 25, 20);
  ellipse(x + 10, y + 10, 25, 20);

  // Face based on expression
  fill(60);
  noStroke();

  // Eyes
  if (mascotExpression === 'happy') {
    stroke(60);
    strokeWeight(2);
    noFill();
    arc(x - 12, y - 5, 10, 8, PI, TWO_PI);
    arc(x + 12, y - 5, 10, 8, PI, TWO_PI);
    noStroke();
  } else if (mascotExpression === 'thinking') {
    fill(60);
    ellipse(x - 12, y - 8, 6, 6);
    ellipse(x + 12, y - 8, 6, 6);
  } else {
    fill(60);
    ellipse(x - 12, y - 5, 6, 6);
    ellipse(x + 12, y - 5, 6, 6);
  }

  // Mouth
  if (mascotExpression === 'happy') {
    stroke(60);
    strokeWeight(2);
    noFill();
    arc(x, y + 10, 20, 15, 0, PI);
  } else if (mascotExpression === 'thinking') {
    fill(60);
    ellipse(x + 8, y + 12, 8, 6);
  } else {
    stroke(60);
    strokeWeight(2);
    line(x - 8, y + 10, x + 8, y + 10);
  }

  // Thought bubble for thinking
  if (mascotExpression === 'thinking') {
    fill(255);
    stroke(180);
    strokeWeight(1);
    ellipse(x + 40, y - 30, 8, 8);
    ellipse(x + 50, y - 45, 12, 12);
    ellipse(x + 65, y - 60, 30, 25);
    fill(100);
    noStroke();
    textSize(14);
    textAlign(CENTER, CENTER);
    text('?', x + 65, y - 62);
  }
}

function drawEndScreen() {
  // Background gradient effect
  for (let i = 0; i < drawHeight; i++) {
    let inter = map(i, 0, drawHeight, 0, 1);
    let c = lerpColor(color(240, 248, 255), color(200, 220, 240), inter);
    stroke(c);
    line(0, i, canvasWidth, i);
  }

  // Title
  fill(30, 60, 90);
  noStroke();
  textSize(32);
  textAlign(CENTER, TOP);
  textStyle(BOLD);
  text('Quiz Complete!', canvasWidth/2, 40);
  textStyle(NORMAL);

  // Score display
  let maxScore = scenarios.length * config.pointsCorrect;
  let scorePercent = floor((score / maxScore) * 100);

  // Score circle
  let cx = canvasWidth/2;
  let cy = 160;
  let radius = 80;

  // Background circle
  fill(255);
  stroke(200);
  strokeWeight(3);
  ellipse(cx, cy, radius * 2, radius * 2);

  // Score arc
  noFill();
  stroke(70, 130, 180);
  strokeWeight(12);
  let angle = map(scorePercent, 0, 100, 0, TWO_PI);
  arc(cx, cy, radius * 1.7, radius * 1.7, -HALF_PI, -HALF_PI + angle);

  // Score text
  fill(30, 60, 90);
  noStroke();
  textSize(36);
  textAlign(CENTER, CENTER);
  textStyle(BOLD);
  text(score, cx, cy - 10);
  textStyle(NORMAL);
  textSize(16);
  text('points', cx, cy + 20);

  // Percentage (below the circle)
  textSize(20);
  fill(70, 130, 180);
  text(scorePercent + '% correct', cx, cy + radius + 20);

  // Performance message
  let message, subMessage;
  let perfMessages = quizData?.endScreen?.performanceMessages;

  if (perfMessages) {
    if (scorePercent >= perfMessages.excellent.threshold) {
      message = perfMessages.excellent.message;
      subMessage = perfMessages.excellent.subMessage;
    } else if (scorePercent >= perfMessages.good.threshold) {
      message = perfMessages.good.message;
      subMessage = perfMessages.good.subMessage;
    } else if (scorePercent >= perfMessages.fair.threshold) {
      message = perfMessages.fair.message;
      subMessage = perfMessages.fair.subMessage;
    } else {
      message = perfMessages.needsWork.message;
      subMessage = perfMessages.needsWork.subMessage;
    }
  } else {
    // Default messages
    if (scorePercent >= 90) {
      message = 'Outstanding!';
      subMessage = 'You have excellent classification skills.';
    } else if (scorePercent >= 70) {
      message = 'Great Job!';
      subMessage = 'You classified most items correctly.';
    } else if (scorePercent >= 50) {
      message = 'Good Progress!';
      subMessage = 'Keep practicing to improve.';
    } else {
      message = 'Keep Learning!';
      subMessage = 'Practice makes perfect.';
    }
  }

  fill(60, 100, 60);
  textSize(24);
  textStyle(BOLD);
  text(message, cx, 290);
  textStyle(NORMAL);

  fill(80);
  textSize(16);
  text(subMessage, cx, 320);

  // Tips section
  fill(255, 255, 255, 200);
  stroke(180);
  strokeWeight(1);
  rect(margin + 50, 340, canvasWidth - 100 - margin, 90, 10);

  let tipsTitle = quizData?.endScreen?.tipsTitle || 'Tips for Success:';
  let tips = quizData?.endScreen?.tips || [
    'Read each scenario carefully before answering.',
    'Look for key characteristics that define each category.',
    'Use hints when stuck—learning is the goal!'
  ];

  fill(70, 100, 130);
  textSize(14);
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  text(tipsTitle, margin + 70, 355);
  textStyle(NORMAL);

  fill(60);
  textSize(13);
  for (let i = 0; i < tips.length; i++) {
    text('• ' + tips[i], margin + 70, 375 + i * 18);
  }

  // Draw happy mascot
  mascotExpression = 'happy';
  drawMascotCharacter(canvasWidth - 100, 150);
}

function mousePressed() {
  if (quizComplete || answered) return;

  // Check if an option was clicked
  for (let btn of optionButtons) {
    if (mouseX > btn.x && mouseX < btn.x + btn.w &&
        mouseY > btn.y && mouseY < btn.y + btn.h) {
      selectAnswer(btn.index);
      return;
    }
  }
}

function selectAnswer(index) {
  if (answered) return;

  selectedAnswer = index;
  answered = true;

  let currentScenario = scenarios[currentScenarioIndex];
  let correctField = config.correctAnswerField;
  let isCorrect = currentScenario.options[index] === currentScenario[correctField];

  // Select and store feedback message once
  let messages;
  if (isCorrect) {
    let points = usedHint ? config.pointsWithHint : config.pointsCorrect;
    score += points;
    feedbackColor = [100, 200, 100];
    mascotExpression = 'happy';
    messages = quizData.encouragingMessages?.correct || ['Correct!'];
  } else {
    feedbackColor = [255, 200, 100];
    mascotExpression = 'thinking';
    messages = quizData.encouragingMessages?.incorrect || ['Not quite.'];
  }
  feedbackMessage = messages[floor(random(messages.length))];
  feedbackAlpha = 100;

  // Show control buttons
  hintButton.hide();
  nextButton.show();
}

function showHint() {
  if (!answered) {
    usedHint = true;
    mascotExpression = 'thinking';
  }
}

function nextScenario() {
  currentScenarioIndex++;

  if (currentScenarioIndex >= scenarios.length) {
    quizComplete = true;
    hideAllButtons();
    restartButton.show();
  } else {
    resetScenarioState();
  }
}

function resetScenarioState() {
  answered = false;
  selectedAnswer = -1;
  usedHint = false;
  mascotExpression = 'neutral';
  feedbackMessage = '';

  hintButton.show();
  nextButton.hide();
}

function restartQuiz() {
  let shuffled = shuffle([...quizData.scenarios]);
  scenarios = shuffled.slice(0, config.questionsPerQuiz);
  currentScenarioIndex = 0;
  score = 0;
  quizComplete = false;
  resetScenarioState();
  restartButton.hide();
}

function hideAllButtons() {
  hintButton.hide();
  nextButton.hide();
}

function windowResized() {
  updateCanvasSize();
  resizeCanvas(canvasWidth, canvasHeight);
  positionButtons();
}

function updateCanvasSize() {
  const container = document.querySelector('main');
  if (container) {
    canvasWidth = min(container.offsetWidth, 900);
  }
}
