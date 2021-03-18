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


export  {
    formatDate
}