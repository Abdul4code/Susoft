export function handler(error){
    // if the error are form related errors. Then return the error data
    if(error.response.status == 400){
        return error.response.data

    // if the error is authentication errors. Then return the user to login page
    }else if(error.response.status == 403){
        router.push({name : 'login'})

    // display the error on the console
    }else{
        console.log(error)
    } 
}

export function get_error_400_messages(error_400){
    let messages = []

    const errorMessages = Object.values(error_400).flat() 
    return errorMessages
}