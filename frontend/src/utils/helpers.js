const formatDate = function(input) {
	if (!input) return null
    let dateObj = new Date(input)
    const year = dateObj.getFullYear()
    const month = (dateObj.getMonth()+1).toString().padStart(2, '0')
    const day = dateObj.getDate().toString().padStart(2, '0')
    const hour = dateObj.getHours().toString().padStart(2, '0')
    const minutes = dateObj.getMinutes().toString().padStart(2, '0')
    return `${day}/${month}/${year} - ${hour}:${minutes}`
}

const formatDateVerbose = function(input, showWeekday=true, showTime=true) {
	if (!input) return null
	var dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    var monthNamesShort = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	let dateObj = new Date(input)
    const year = dateObj.getFullYear()
    const month = monthNamesShort[dateObj.getMonth()]
    const day = dateObj.getDate().toString().padStart(2, '0')
    const dayName = dayNames[dateObj.getDay()]

    const hour = dateObj.getHours().toString().padStart(2, '0')
    const minutes = dateObj.getMinutes().toString().padStart(2, '0')

    let weekday = showWeekday ? `${dayName}, ` : ''
   	let time = showTime ? `, ${hour}:${minutes}` : ''

    return weekday + `${day} ${month} ${year}`	+ time
}

export  {
    formatDate,
    formatDateVerbose
}