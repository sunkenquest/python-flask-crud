import { useState, useEffect } from 'react'

const useContacts = () => {
    const [contacts, setContacts] = useState([])

    useEffect(() => {
        const fetchContacts = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/contacts")
                const data = await response.json()
                setContacts(data.contacts)

            } catch (error) {
                console.error("Failed to fetch contacts:", error)
            }
        }

        fetchContacts()
    }, [])

    return contacts
}

export default useContacts
