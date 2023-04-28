'use strict'

/* -----------------------------------
   * Start * Toggle Dark / Light Mode
* ------------------------------------ */
// check if the user has a saved preference for dark mode
if (localStorage.getItem('isDarkMode') === 'true') {
  $('body').addClass('is-dark');
  $('#toggle-mode, #mobile-toggle').html(`<svg width="24" height="24" viewBox="0 0 24 24" class="icon stroke-white"><path d="M12 19a7 7 0 1 0 0-14 7 7 0 0 0 0 14z"></path><path d="M15.899 12.899a4 4 0 0 1-4.797-4.797A4.002 4.002 0 0 0 12 16c1.9 0 3.49-1.325 3.899-3.101z"></path><path d="M12 5V3M12 21v-2"></path><path d="M5 12H2h3zM22 12h-3 3zM16.95 7.05L19.07 4.93 16.95 7.05zM4.929 19.071L7.05 16.95 4.93 19.07zM16.95 16.95l2.121 2.121-2.121-2.121zM4.929 4.929L7.05 7.05 4.93 4.93z"></path></svg>`);
} else {
  $('body').removeClass('is-dark');
  $('#toggle-mode, #mobile-toggle').html(`<svg role="img" width="24" height="24" viewBox="0 0 24 24" class="icon stroke-white"><circle cx="12" cy="12" r="4"></circle><path d="M12 5L12 3M12 21L12 19M5 12L2 12 5 12zM22 12L19 12 22 12zM16.9497475 7.05025253L19.0710678 4.92893219 16.9497475 7.05025253zM4.92893219 19.0710678L7.05025253 16.9497475 4.92893219 19.0710678zM16.9497475 16.9497475L19.0710678 19.0710678 16.9497475 16.9497475zM4.92893219 4.92893219L7.05025253 7.05025253 4.92893219 4.92893219z"></path></svg>`);
}

/* -----------------------------------
   * Start * Toggle Dark / Light Mode
* ------------------------------------ */
$('#toggle-mode, #mobile-toggle').click(function() {
  let $elem = $('body');
  if ($elem.hasClass('is-dark')) {
    $elem.removeClass('is-dark');
    $(this).html(`<svg role="img" width="24" height="24" viewBox="0 0 24 24" class="icon stroke-white"><circle cx="12" cy="12" r="4"></circle><path d="M12 5L12 3M12 21L12 19M5 12L2 12 5 12zM22 12L19 12 22 12zM16.9497475 7.05025253L19.0710678 4.92893219 16.9497475 7.05025253zM4.92893219 19.0710678L7.05025253 16.9497475 4.92893219 19.0710678zM16.9497475 16.9497475L19.0710678 19.0710678 16.9497475 16.9497475zM4.92893219 4.92893219L7.05025253 7.05025253 4.92893219 4.92893219z"></path></svg>`);
    localStorage.setItem('isDarkMode', 'false');
  } else {
    $elem.addClass('is-dark');
    $(this).html(`<svg width="24" height="24" viewBox="0 0 24 24" class="icon stroke-white"><path d="M12 19a7 7 0 1 0 0-14 7 7 0 0 0 0 14z"></path><path d="M15.899 12.899a4 4 0 0 1-4.797-4.797A4.002 4.002 0 0 0 12 16c1.9 0 3.49-1.325 3.899-3.101z"></path><path d="M12 5V3M12 21v-2"></path><path d="M5 12H2h3zM22 12h-3 3zM16.95 7.05L19.07 4.93 16.95 7.05zM4.929 19.071L7.05 16.95 4.93 19.07zM16.95 16.95l2.121 2.121-2.121-2.121zM4.929 4.929L7.05 7.05 4.93 4.93z"></path></svg>`);
    localStorage.setItem('isDarkMode', 'true');
  }
});

const startLoadingBar = () => {
  $("#loading-bar").show().width((50 + Math.random() * 30) + '%');
}

const stopLoadingBar = () => {
  $("#loading-bar").width("101%").delay(200).fadeOut(400, () => {
      $(this).width("0");
  });
}

/* ----------------------------
   * Start * Preloader Service
* ----------------------------- */
$(document).ready(function () {
  startLoadingBar();
  stopLoadingBar();
});

/* -----------------------
   * Start * Toast Service
* --------------------- */
const showMessage = (text) => {
  iziToast.show({
    maxWidth: '280px',
    class: 'success-toast',
    icon: 'fas fa-check-circle',
    title: '',
    message: text,
    titleColor: '#fff',
    messageColor: '#fff',
    iconColor: '#fff',
    backgroundColor: '#1db9f0',
    progressBarColor: '#fafafa',
    position: 'bottomRight',
    transitionIn: 'fadeInUp',
    close: true,
    timeout: 3500,
    zindex: 99999
  });
}

const showError = (text) => {
  iziToast.show({
    maxWidth: '280px',
    class: 'error-toast',
    icon: 'far fa-ban',
    title: '',
    message: text,
    titleColor: '#fff',
    messageColor: '#fff',
    iconColor: '#fff',
    backgroundColor: '#ff533d',
    progressBarColor: '#fff',
    position: 'bottomRight',
    transitionIn: 'fadeInUp',
    close: true,
    timeout: 3500,
    zindex: 99999
  });
}
/* -----------------------
   * End * Toast Service
* --------------------- */

/* --------------------------
   * Start * UI Tabs Service
* --------------------------- */
$(document).ready(function () {
$(".uk-tab").find("li").click(function() {
  $(".uk-tab").find("li").removeClass("uk-active");
  $(this).addClass("uk-active");
});
});

$(function() {
var cropper = null;
const token = $('meta[name="token"]').attr('content');

/* --------------------------
   * Start * Preview Files
* --------------------------- */
$('#file').on('change', function(e) {
  var input = $(this)[0];
  if (input.files && input.files[0]) {
    let file = $(this).prop('files')[0];
    var reader = new FileReader();
    reader.onloadstart = function(e) {
      startLoadingBar();
    }
    reader.onload = function(e) {
      if (file.type.startsWith('image/')) {
        if (file.size > 5 * 1024 * 1024) {
            $(this).val(''); // Clear the file input field
            $('#crop-preview').attr('src', '');
            showError('The selected image file is too large.');
            UIkit.modal($('#crop-modal')).hide();
        } else {
            // the selected file is an image
            $('#crop-preview').attr('src', e.target.result);
            // Shows the crop modal
            UIkit.modal($('#crop-modal')).show();
            if (cropper !== null) {
              cropper.destroy();
            }
            cropper = new Cropper($('#crop-preview')[0], {
              aspectRatio: 0,
              viewMode: 1,
              autoCropArea: 1,
            });
            // hide the video preview element
            $('#video-preview').hide();
        }
      } else if (file.type.startsWith('video/')) {
          if (file.type.startsWith('video/')) {
            if (file.size > 30 * 1024 * 1024) {
              $(this).val(''); // Clear the file input field
              $('#video-preview').attr('src', '');
              showError('The selected video file is too large.');
              UIkit.modal($('#video-modal')).hide();
            } else {
              // the selected file is a video and is under the size limit
              $('#video-preview').attr('src', e.target.result);
              // Shows the video modal
              UIkit.modal($('#video-modal')).show();
            }
          }
      } else {
        // the selected file is neither an image nor a video
        $(input).val('');
        $('#crop-preview').hide();
        $('#video-preview').hide();
      }
    }
    reader.onloadend = function(e) {
      stopLoadingBar();
    }
    reader.readAsDataURL(input.files[0]);
  }
});

/* --------------------------------
   * Start * Handles Images Upload
* --------------------------------- */
$('#image-form').on('submit', function(e) {
  // prevent default form submit
  e.preventDefault();

  if (cropper !== null) {
    const formData = new FormData(this);
    let canvas = cropper.getCroppedCanvas();
    canvas.toBlob((image) => {
    // append the cropped image data to the FormData object
    formData.append('file', image, 'content.jpg');
    startLoadingBar();
    fetch('/upload', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
        'X-CSRFToken': token,
      }
    })
    .then(response => {
      if (response.ok) {
        // Handle the successful response from the backend
        return response.json()
      } else {
        throw new Error('Upload failed');
      }
    })
    .then(data => {
      // handle successful upload
      if (data.status == 200) {
        // destroy the Cropper instance
        cropper.destroy();
        cropper = null;
        $('#crop-preview').attr('src', '');
        $('#upload-form').trigger('reset');
        UIkit.modal($('#crop-modal')).hide();
        showMessage(data.message);
        stopLoadingBar();
      } else {
        showError(data.message);
      }
    })
    .catch(error => {
      // Handle the error case
      console.error('Error:', error);
    });

    }, 'image/jpeg');
  }
});

/* ---------------------------------
   * Start * Handles Videos Upload
* ---------------------------------- */
$('#video-form').on('submit', function(e) {
  // prevent default form submit
  e.preventDefault();

    const formData = new FormData(this);
    const file = $('#file').prop('files')[0];
    formData.append('file', file);

    fetch('/upload', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json',
        'X-CSRFToken': token,
      }
    })
    .then(response => {
      if (response.ok) {
        // Handle the successful response from the backend
        return response.json()
      } else {
        throw new Error('Upload failed');
      }
    })
    .then(data => {
      // handle successful upload
      if (data.status == 200) {
        alert(data.message);
        $('#video-form').trigger('reset');
        UIkit.modal($('#video-modal')).hide();
        showMessage(data.message);
      } else {
        showError(data.message);
      }
    })
    .catch(error => {
      // Handle the error case
      console.error('Error:', error);
    });
});

/* ---------------------------------
   * Start * Copy text to clipboard
* ---------------------------------- */
$('.media-options a.is-share').click(function() {
  let text = $(this).data('link');
  copyToClipboard(text);
});


/* -----------------------------
   * Start * Handles Like Post
* ------------------------------ */
$(document).on('click', '.photo-like', function(e) {
  e.preventDefault();
  let target = $(this).data('id');
  let formData = new FormData();
  formData.append('target', target);

  fetch('/like', {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': token,
    }
  })
  .then(response => {
    if (response.ok) {
      // Handle the successful response from the backend
      return response.json()
    } else {
      throw new Error('An error occurred!');
    }
  })
  .then(data => {
    // handle successful upload
    if (data.status == 200 && data.action == 1) {
      $(this).addClass('is-liked');
      $(this).children('span').text(data.count);
    } else if (data.status == 200 && data.action == 0) {
      $(this).removeClass('is-liked');
      $(this).children('span').text(data.count);
    } else {
      console.error('An error occurred!');
    }
  })
  .catch(error => {
    // Handle the error case
    console.error('Error:', error);
  });
});

/* -----------------------------
   * Start * Handles Like Post
* ------------------------------ */
$(document).on('click', '.is-like-button', function(e) {
  e.preventDefault();
  let target = $(this).data('id');
  let formData = new FormData();
  formData.append('target', target);

  fetch('/like', {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': token,
    }
  })
  .then(response => {
    if (response.ok) {
      // Handle the successful response from the backend
      return response.json()
    } else {
      throw new Error('An error occurred!');
    }
  })
  .then(data => {
    // handle successful upload
    if (data.status == 200 && data.action == 1) {
      $(this).addClass('is-liked');
      $(this).next().find('span.count').text(data.count);
    } else if (data.status == 200 && data.action == 0) {
      $(this).removeClass('is-liked');
      $(this).next().find('span.count').text(data.count);
    } else {
      console.error('An error occurred!');
    }
  })
  .catch(error => {
    // Handle the error case
    console.error('Error:', error);
  });
});

/* -----------------------------
   * Start * Handles Like Comment
* ------------------------------ */
$(document).on('click', '.is-comment-like-btn', function(e) {
  e.preventDefault();
  let target = $(this).data('id');
  let formData = new FormData();
  formData.append('target', target);

  fetch('/like/comment', {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': token,
    }
  })
  .then(response => {
    if (response.ok) {
      // Handle the successful response from the backend
      return response.json()
    } else {
      throw new Error('An error occurred!');
    }
  })
  .then(data => {
    // handle successful upload
    if (data.status == 200 && data.action == 1) {
      $(this).addClass('is-liked');
      $(this).next().find('div.count').text(data.count);
    } else if (data.status == 200 && data.action == 0) {
      $(this).removeClass('is-liked');
      $(this).next().find('div.count').text(data.count);
    } else {
      console.error('An error occurred!');
    }
  })
  .catch(error => {
    // Handle the error case
    console.error('Error:', error);
  });
});

/* -----------------------------------
   * Start * Handles Comment Posting
* ------------------------------------ */
$(document).on('click', '#submit-comment', function(e) {
  e.preventDefault();
  let target = $(this).data('link');
  let comment = $('textarea[name="comment"]').val();
  let media = $('#comment-media').prop('files')[0];
  let formData = new FormData();
  formData.append('target', target);
  formData.append('comment', comment);
  formData.append('media', media);

  fetch('/comment', {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      'X-CSRFToken': token,
    }
  })
  .then(response => {
    if (response.ok) {
      // Handle the successful response from the backend
      return response.json()
    } else {
      throw new Error('An error occurred!');
    }
  })
  .then(data => {
    // handle successful upload
    if (data.status == 200) {
      $('#placeholder').fadeOut().detach();
      $('.media-replies-wrapper').find('h3').text(`${data.count} comments`);
      $('.media-replies-wrapper').append(data.comment);
      showMessage(data.message);
    } else {
      showError(data.message);
    }
  })
  .catch(error => {
    // Handle the error case
    console.error('Error:', error);
  });
});


});

/* ---------------------------------
   * Start * Copy text to clipboard
* ---------------------------------- */
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    showMessage('Link copied to clipboard!');
  }, () => {
    showError('Failed to copy link to clipboard!');
  });
}

/* ---------------------------
   * Start * Init. Type Effect
* ---------------------------- */
const typed = new Typed('#intro-text', {
  strings: [`Welcome to SnapShots, the ultimate image sharing platform.`, `Explore a vast collection of contents uploaded by people, and connect with people from around the world.`, `Share images and videos with people all around the world.`],
  showCursor: false,
  loop: true,
  typeSpeed: 30,
  backDelay: 900,
  backspeed: 30
});