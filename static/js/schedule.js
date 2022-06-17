// set start and end time to be after current time
const now = new Date();
// update hour using timezone offset (minutes)
now.setHours(now.getHours() - now.getTimezoneOffset()/60);
const nowStr = now.toISOString().substring(0,16);
// console.log(now, nowStr);

const startTime = document.querySelector('#datetime_start');
startTime.min = nowStr;
const endTime = document.querySelector('#datetime_end');
endTime.min = nowStr;

// retrieve available reservations by sending AJAX request to sever
document.querySelector('#schedule').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formData = {
        'startTime': document.querySelector('[name="start_time"]').value,
        'endTime': document.querySelector('[name="end_time"]').value
    };

    const queryString = new URLSearchParams(formData).toString();

    fetch(`/search_reservations?${queryString}`)
        .then(response => response.json())
        .then(res => {
            if (res.length === 0) {
                document.getElementById('reservation_text').innerHTML 
                    = 'Sorry, there is no availability at these times, try another search :(';  
            }
            else {
                document.getElementById('reservation_text').innerHTML 
                    = 'Below is the current availability. Select a time that works for you!';
                for (time of res) {
                    const betterTime = time.slice(0, time.length - 4);
                    console.log(betterTime);
                    document.getElementById('available_reservations').insertAdjacentHTML(
                        'beforeend',
                        `<form action="/reservations/book" method="POST">
                        <input value="${betterTime}" name='start_time' type='submit' class='schedule_res'>
                        </form>`);
                }
            }
        })

})

