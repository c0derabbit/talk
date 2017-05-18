window.onload = () => {
  const inputField = document.querySelector('input[type="text"]');
  inputField && inputField.focus();

  const messageList = document.querySelector('.messages');
  if (messageList) {
    messageList.scrollTop = messageList.scrollHeight;
  }

  const messageInput = document.querySelector('textarea');
  if (messageInput) {
    messageInput.onkeypress = (key) => {
      if (!key.shiftKey && key.which == 13) {
        send_message.submit();
      }
    }
  }
}
