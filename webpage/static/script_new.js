// Function to handle login process
function login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Perform authentication logic here
    // For simplicity, let's assume the credentials are hardcoded
    if (username === "JohnDoe" && password === "123") {
        // Save the logged-in user's username to local storage
        localStorage.setItem("loggedInUser", username);
        window.location.href = "course.html"; // Redirect to the dashboard
    } else {
        alert("Invalid username or password");
    }
}

function stream(stream){
    window.location.href = "http://localhost:8501"
}
function loadCourse(youtubeLink) {
    window.location.href = youtubeLink;
}

function completeCourse(courseName) {
    // Award 50 points for completing the course
    var currentExperience = parseInt(document.getElementById('experience').innerText.split(' ')[2]);
    var newExperience = currentExperience + 20;
    document.getElementById('experience').innerText = 'Total Experience: ' + newExperience;

    // Update progress bar
    // var progress = 20; // Assuming 200 exp is the maximum
    if (newExperience<=100){
        document.querySelector('#progress').style.width = newExperience + '%';
        document.getElementById('progress').innerText = newExperience + '%';
    } 

    // Update leaderboard with new experience
    var username = document.getElementById('username').innerText;
    var leaderboardList = document.getElementById('leaderboard-list');
    var leaderboardEntries = leaderboardList.getElementsByTagName('li');

    for (var i = 0; i < leaderboardEntries.length; i++) {
        var entryUser = leaderboardEntries[i].querySelector('.leaderboard-user').innerText;
        if (entryUser === username) {
            leaderboardEntries[i].querySelector('.leaderboard-exp').innerText = newExperience + ' exp';
            break;
        }
    }
}

function selectCourse(courseName) {
    // Redirect to the course page with courseName as a parameter
    window.location.href = `course.html?course=${courseName}`;
}

function selectTopic(topicName) {
    // Redirect to the topic page with topicName as a parameter
    window.location.href = `topic.html?topic=${topicName}`;
}

document.addEventListener('DOMContentLoaded', function() {
    // Simulated user data
    const userData = {
        username: "JohnDoe",
        totalExperience: 0,
        courseProgress: 0 // Example: 70% progress
    };

    // Update user information
    document.getElementById('username').textContent = `Username: ${userData.username}`;
    document.getElementById('experience').textContent = `Total Experience: ${userData.totalExperience}`;
    document.querySelector('.progress').style.width = `${userData.courseProgress}%`;
});

function loadAssignment(assignmentNumber) {
    var assignmentContent = document.getElementById('assignment-content');

    // Clear previous assignment content
    assignmentContent.innerHTML = '';

    // Load content based on assignment number
    switch(assignmentNumber) {
        case 1:
            assignmentContent.innerHTML = "<li><input type=\"radio\" name=\"mcq1\" value=\"option1\"> Option 1</li><li><input type=\"radio\" name=\"mcq1\" value=\"option2\"> Option 2</li><li><input type=\"radio\" name=\"mcq1\" value=\"option3\"> Option 3</li><li><input type=\"radio\" name=\"mcq1\" value=\"option4\"> Option 4</li>";
            // Load other content for Assignment 1
            break;
        case 2:
            assignmentContent.innerHTML = "<h2>Assignment 2</h2><p>Description for Assignment 2</p>";
            // Load other content for Assignment 2
            break;
        case 3:
            assignmentContent.innerHTML = "<h2>Assignment 3</h2><p>Description for Assignment 3</p>";
            // Load other content for Assignment 3
            break;
        default:
            assignmentContent.innerHTML = "<p>No assignment found</p>";
    }
}