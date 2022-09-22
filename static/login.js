function sign_in() {
  let username = $('#input-username').val();
  let password = $('#input-password').val();

  if (username == '') {
    $('#help-id-login').text('아이디를 입력해주세요.');
    $('#input-username').focus();
    return;
  } else {
    $('#help-id-login').text('');
  }

  if (password == '') {
    $('#help-password-login').text('비밀번호를 입력해주세요.');
    $('#input-password').focus();
    return;
  } else {
    $('#help-password-login').text('');
  }
  $.ajax({
    type: 'POST',
    url: '/sign_in',
    data: {
      username_give: username,
      password_give: password,
    },
    success: function (response) {
      if (response['result'] == 'success') {
        $.cookie('mytoken', response['token'], { path: '/' });
        window.location.replace('/');
      } else {
        alert(response['msg']);
      }
    },
  });
}

function sign_up() {
  let username = $('#input-username').val();
  let password = $('#input-password').val();
  let password2 = $('#input-password2').val();
  console.log(username, password, password2);

  if ($('#help-id').hasClass('is-danger')) {
    alert('아이디를 다시 확인해주세요.');
    return;
  } else if (!$('#help-id').hasClass('is-success')) {
    alert('아이디 중복확인을 해주세요.');
    return;
  }

  if (password == '') {
    $('#help-password')
      .text('비밀번호를 입력해주세요.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password').focus();
    return;
  } else if (!is_password(password)) {
    $('#help-password')
      .text(
        '비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자'
      )
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password').focus();
    return;
  } else {
    $('#help-password')
      .text('사용할 수 있는 비밀번호입니다.')
      .removeClass('is-danger')
      .addClass('is-success');
  }
  if (password2 == '') {
    $('#help-password2')
      .text('비밀번호를 입력해주세요.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password2').focus();
    return;
  } else if (password2 != password) {
    $('#help-password2')
      .text('비밀번호가 일치하지 않습니다.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-password2').focus();
    return;
  } else {
    $('#help-password2')
      .text('비밀번호가 일치합니다.')
      .removeClass('is-danger')
      .addClass('is-success');
  }
  $.ajax({
    type: 'POST',
    url: '/sign_up/save',
    data: {
      username_give: username,
      password_give: password,
    },
    success: function (response) {
      alert('회원가입을 축하드립니다!');
      window.location.replace('/login');
    },
  });
}

/*로그인 <-> 회원가입 창 변경 토글*/
function toggle_sign_up() {
  $('#sign-up-box').toggleClass('is-hidden');
  $('#div-sign-in-or-up').toggleClass('is-hidden');
  $('#btn-check-dup').toggleClass('is-hidden');
  $('#help-id').toggleClass('is-hidden');
  $('#help-password').toggleClass('is-hidden');
  $('#help-password2').toggleClass('is-hidden');
}
/*회원가입하러가기 버튼 클릭 시 초기화*/
function click_gosignup_btn() {
  $('#help-id-login').text('');
  $('#input-username').val('');
  $('#input-password').val('');
  $('#input-password2').val('');
}
/*취소 버튼 클릭 시 초기화*/
function click_cancel_btn() {
  $('#help-id')
    .text(
      '아이디는 2-10자의 영문과 숫자와 일부 특수문자(._-)만 입력 가능합니다.'
    )
    .removeClass('is-danger')
    .removeClass('is-success')
    .addClass('is-safe');
  $('#help-password')
    .text(
      '영문과 숫자 조합의 8-20자의 비밀번호를 설정해주세요. 특수문자(!@#$%^&*)도 사용 가능합니다.'
    )
    .removeClass('is-danger')
    .removeClass('is-success')
    .addClass('is-safe');
  $('#help-password2')
    .text('비밀번호를 다시 한 번 입력해주세요.')
    .removeClass('is-danger')
    .removeClass('is-success')
    .addClass('is-safe');
  $('#input-username').val('');
  $('#input-password').val('');
  $('#input-password2').val('');
}

/*아이디 양식 확인*/
function is_nickname(asValue) {
  var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
  return regExp.test(asValue);
}
/*비밀번호 양식 확인*/
function is_password(asValue) {
  var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
  return regExp.test(asValue);
}

/*ID 중복확인*/
function check_dup() {
  let username = $('#input-username').val();
  console.log(username);
  if (username == '') {
    $('#help-id')
      .text('아이디를 입력해주세요.')
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-username').focus();
    return;
  }
  if (!is_nickname(username)) {
    $('#help-id')
      .text(
        '아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이'
      )
      .removeClass('is-safe')
      .addClass('is-danger');
    $('#input-username').focus();
    return;
  }
  $('#help-id').addClass('is-loading');
  $.ajax({
    type: 'POST',
    url: '/sign_up/check_dup',
    data: {
      username_give: username,
    },
    success: function (response) {
      if (response['exists']) {
        $('#help-id')
          .text('이미 존재하는 아이디입니다.')
          .removeClass('is-safe')
          .addClass('is-danger');
        $('#input-username').focus();
      } else {
        $('#help-id')
          .text('사용할 수 있는 아이디입니다.')
          .removeClass('is-danger')
          .addClass('is-success');
      }
      $('#help-id').removeClass('is-loading');
    },
  });
}
