
const sendHttpRequest = (method, url, data) => {
  const promise = new Promise((resolve, reject) =>{
    const xhr = new XMLHttpRequest();
    xhr.open(method, url);

    xhr.responseType = 'json';
    if(data){
      xhr.setRequestHeader('Content-Type', 'text/json');
    }
    xhr.onload = () => {
      resolve(xhr.response);
    };
    xhr.send(JSON.stringify(data));
  });
  return promise;
}

const getData = () => {
  sendHttpRequest('GET', 'http://localhost:8080/getAll').then(responseData => {
    show(responseData);
  });
}

const sendData = (data) => {
  document.getElementById(data).parentNode.style.display = 'none';
  document.getElementById("students").style.display = 'block';
  document.getElementById("studentInfo").style.display = 'none';
  sendHttpRequest('POST', 'http://localhost:8080/delete', {'id': data}).then(responseData => {
      console.log(responseData);
    })
    .catch(err => {
      console.log(err);
    });
}



function show(data){
  const ul = document.getElementById('one')
  var li = ''
  for(i=0;i<=data.length;i++){
    if(data[i]){
      li += '<li>';
      li += '<div id="' + data[i].name+' '+data[i].age+' '+data[i].id +'" onclick="showStudentInfo(id)">'
      li += '<h2>'+ data[i].name + '</h2>';
      li += '<h3>'+ data[i].age + '</h3>';
      li += '</div>';
      li += '<button id="'+ data[i].id + '" onclick="sendData(id)">Delete</button>' ;
      li += '</li>';
    }
  }
  ul.innerHTML += li;
}

function showStudentInfo(id){
  var html = '';
  document.getElementById("students").style.display = 'none';
  const student = document.getElementById(id).id.split(' ');
  html += '<h1> Name: ' + student[0] + '</h1>'
  html += '<h2>     Age: ' + student[1] + '</h2>'
  html += '<h2>     ID: ' + student[2] + '</h2>'
  html += '<button name="'+ student[2] + '" onclick="sendData(name)">Delete</button>';
  html += '<button onclick="showAllStudents()">Go Back</button>';
  const studentInfo = document.getElementById('studentInfo');
  studentInfo.style.display = 'block';
  studentInfo.innerHTML = html;
}

function showAllStudents(){
  document.getElementById('studentInfo').style.display = 'none';
  document.getElementById("students").style.display = 'block';
}

getData()