

document.querySelectorAll('.course').forEach(course => {
    course.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
        const courseName = this.getAttribute('data-course-name');
        // completeCourse(courseName);
        // Optionally, navigate to the topic page after loading content
        window.location.href = this.querySelector('a').getAttribute('data-course-url');
    });
});





function updateDashboardData(dash) {
        if(!dash){
            fetch('/dashboard-data')
            .then(response => response.json())
            .then(data => {
                // Update leaderboard
                let leaderboardList = document.getElementById('leaderboard-list');
                leaderboardList.innerHTML = '';
                data.leaderboard.forEach((entry, index) => {
                    let listItem = document.createElement('li');
                    listItem.textContent = `${entry.student_name}: ${entry.exp_points} points`;
                    leaderboardList.appendChild(listItem);
                });
      
                // Update progress bar
                let progressBar = document.getElementById('progress');
                if (data.exp_points !== null) {
                    progressBar.style.width = `${data.progress_percentage}%`;
                    progressBar.textContent = `${data.progress_percentage}%`;
                    document.getElementById('experience').innerText = 'Total Experience: ' + `${data.exp_points}`;
                } else {
                    console.error('Error fetching progress percentage:', data.error);
                }
            })
            .catch(error => console.error('Error fetching dashboard data:', error));
        } 
        else {
            fetch('/dashboard-data')
            .then(response => response.json())
            .then(data => {     
                // Update progress bar
                let progressBar = document.getElementById('progress');
                if (data.exp_points !== null) {
                    progressBar.style.width = `${data.progress_percentage}%`;
                    progressBar.textContent = `${data.progress_percentage}%`;
                    document.getElementById('experience').innerText = `${data.exp_points}`;
                } else {
                    console.error('Error fetching progress percentage:', data.error);
                }
            })
            .catch(error => console.error('Error fetching dashboard data:', error));
        }
  }
  






function checkAndCompleteAssignment( assignmentNumber, assignment_name, topic_id) {
    const studentId = document.getElementById('student-id').value;


    fetch('/check-assignment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            // assignment_number: assignment_id,
            assignment_name: assignment_name,
            topic_id: topic_id,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.completed) {
            alert('Assignment already completed!');
        } else {
            console.log("Assign Number: ", assignmentNumber);
            console.log("Assign Name: ", assignment_name);
            completeAssignment(assignmentNumber, assignment_name, topic_id);
        }
    })
    .catch(error => console.error('Error checking assignment:', error));
}





function completeAssignment(assignmentNumber, assignment_name, topic_id) {
    const studentId = document.getElementById('student-id').value;

    fetch('/complete-assignment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            assignment_number: assignmentNumber,
            assignment_name: assignment_name,
            topic_id: topic_id,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log( 'Topic ID: ', topic_id)
            // updateProgressBar(data.progress_percentage);
            // updateLeaderboard();
            // updateDashboardData();
            console.log("Assignment Completed")
        } else {
            console.error('Error completing assignment:', data.error);
        }
    })
    .catch(error => console.error('Error completing assignment:', error));
}


