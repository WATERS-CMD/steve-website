// Function to fetch and display the posts
function getPosts() {
  fetch('/posts')
      .then(response => response.json())
      .then(data => {
          const postsContainer = document.getElementById('postsContainer');
          postsContainer.innerHTML = '';

          data.forEach(post => {
              const postElement = document.createElement('div');
              postElement.classList.add('post');

              const usernameElement = document.createElement('p');
              usernameElement.textContent = 'Username: ' + post.username;
              postElement.appendChild(usernameElement);

              const dateElement = document.createElement('p');
              dateElement.textContent = 'Date: ' + post.created_at;
              postElement.appendChild(dateElement);

              const descriptionElement = document.createElement('p');
              descriptionElement.textContent = 'Description: ' + post.description;
              postElement.appendChild(descriptionElement);

              if (post.is_admin) {
                  const actionsElement = document.createElement('div');
                  actionsElement.classList.add('actions');

                  const editButton = document.createElement('button');
                  editButton.textContent = 'Edit';
                  editButton.addEventListener('click', () => editPost(post.id));
                  actionsElement.appendChild(editButton);

                  const deleteButton = document.createElement('button');
                  deleteButton.textContent = 'Delete';
                  deleteButton.addEventListener('click', () => deletePost(post.id));
                  actionsElement.appendChild(deleteButton);

                  postElement.appendChild(actionsElement);
              }

              postsContainer.appendChild(postElement);
          });
      })
      .catch(error => console.error(error));
}

// Function to handle post editing
function editPost(postId) {
  const newDescription = prompt('Enter a new description:');
  if (newDescription !== null) {
      fetch(`/edit_post/${postId}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ description: newDescription })
      })
      .then(response => response.json())
      .then(data => {
          console.log(data);
          getPosts(); // Refresh the posts after editing
      })
      .catch(error => console.error(error));
  }
}

// Function to handle post deletion
function deletePost(postId) {
  if (confirm('Are you sure you want to delete this post?')) {
      fetch(`/delete_post/${postId}`, {
          method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
          console.log(data);
          getPosts(); // Refresh the posts after deletion
      })
      .catch(error => console.error(error));
  }
}

// Fetch and display the posts on page load
getPosts();
