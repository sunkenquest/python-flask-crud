import useContacts from '../../hooks/useContacts'
const Content = () => {
    const contacts = useContacts()

    return (
        <div>
            <h1>Contacts</h1>
            <ul>
                {contacts.length > 0 ? (
                    contacts.map((contact, index) => (
                        <li key={index}>
                            <p><strong>Name:</strong> {contact.firstName} {contact.lastName}</p>
                            <p><strong>Email:</strong> {contact.email}</p>
                        </li>
                    ))
                ) : (
                    <p>Loading contacts...</p>
                )}
            </ul>
        </div>
    )
}

export default Content
