function sign_out() {
  $.removeCookie('mytoken', { path: '/' });
  alert('๋ก๊ทธ์์!');
  window.location.href = '/';
}
