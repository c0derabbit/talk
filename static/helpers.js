window.onload = () => {
  const inputField = document.querySelector('input');
  inputField && inputField.focus();

  const messageInput = document.querySelector('textarea');
  messageInput.onkeypress = (key) => {
    if (!key.shiftKey && key.which == 13) {
      send_message.submit();
    }
  }

  const messageList = document.querySelector('.messages');
  messageList.scrollTop = messageList.scrollHeight;
}
