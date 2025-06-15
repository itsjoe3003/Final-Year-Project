
function stream(stream){
    window.location.href = "http://localhost:8501"
}
function loadCourse(youtubeLink) {
    window.location.href = youtubeLink;
}





function selectCourse(courseName) {
    // Redirect to the course page with courseName as a parameter
    window.location.href = `course.html?course=${courseName}`;
}

function selectTopic(topicName) {
    // Redirect to the topic page with topicName as a parameter
    window.location.href = `topic.html?topic=${topicName}`;
}



function loadAssignment(assignmentNumber) {
    var assignmentContent = document.getElementById('assignment-content');

    // Clear previous assignment content
    assignmentContent.innerHTML = '';

    // Load content based on assignment number
    switch(assignmentNumber) {
        case 1:
            // assignmentContent.innerHTML = "<li><input type=\"radio\" name=\"mcq1\" value=\"option1\"> Option 1</li><li><input type=\"radio\" name=\"mcq1\" value=\"option2\"> Option 2</li><li><input type=\"radio\" name=\"mcq1\" value=\"option3\"> Option 3</li><li><input type=\"radio\" name=\"mcq1\" value=\"option4\"> Option 4</li>";
            // Load other content for Assignment 1
            assignmentContent.innerHTML = "<h2>Assignment 1</h2><p> MCQ stuff</p>";

            break;
        case 2:
            assignmentContent.innerHTML = "<h2>Assignment 2</h2><p> Fill in the blank stuff</p>";
            // Load other content for Assignment 2
            break;
        case 3:
            assignmentContent.innerHTML = "<h2>Assignment 3</h2><p>Match the following stuff</p>";
            // Load other content for Assignment 3
            break;
        default:
            assignmentContent.innerHTML = "<p>No assignment found</p>";
    }
}



// Function to load content dynamically based on query parameter
function loadContent(course) {
    // var urlParams = new URLSearchParams(window.location.search);
    // var course = urlParams.get('course');

    var topics = {
        'Course 1': {
            name: 'Topic 1',
            video: 'https://youtu.be/fh4RNP4bMWk?si=v5vfqOQOrEkoj5Qe',
            description: 'Description of Topic 1',
        },
        'Course 2': {
            name: 'Topic 2',
            video: 'https://www.youtube.com/watch?v=JxkyEcSGLYY',
            description: 'Description of Topic 2',
        },
        'Course 3': {
            name: 'Topic 3',
            video: 'https://www.youtube.com/watch?v=JxkyEcSGLYY',
            description: 'Description of Topic 3',
        }
    };

    // Populate topic content based on selected course
    var topic = topics[course];
    document.getElementById('')
    document.getElementById('topic-name').textContent = topic.name;
    document.getElementById('video-iframe').src = topic.video;
    document.getElementById('topic-description').textContent = topic.description;
    


}

