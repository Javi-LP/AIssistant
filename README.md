# AIssistant
En este proyecto, he desarrollado un chatbot denominado AIssistant, cuyo propósito es permitir que los usuarios interactúen de manera intuitiva y obtengan información tanto sobre mi experiencia profesional como algunos detalles personales. El chatbot está construido utilizando la plataforma LangChain y el modelo GPT-4, lo que permite una integración eficiente de procesamiento de lenguaje natural (NLP).

Cada vez que un usuario realiza una consulta, el sistema implementa un proceso de Recuperación-Augmentación-Generación (RAG). En este proceso, la pregunta es vectorizada y se extraen N líneas relevantes de una ventana de contexto predefinida, optimizando la precisión de las respuestas. Esta información contextualizada se envía al modelo de lenguaje GPT-4, junto con la pregunta original, para generar una respuesta informada y precisa.

El chatbot también incluye un robusto sistema de gestión de usuarios basado en códigos de acceso, donde cada usuario recibe un token de acceso con un número limitado de usos. Estos tokens permiten controlar el acceso y la interacción con la plataforma de manera segura y eficiente. La información relativa a los accesos y la gestión de usuarios se almacena en una base de datos PostgreSQL, lo que asegura una administración adecuada y escalable del sistema.

El servicio está desplegado como una API utilizando FastAPI, lo que facilita su integración con otras aplicaciones y servicios. Este enfoque APIficado permite que terceros puedan interactuar con el chatbot de manera sencilla a través de solicitudes HTTP, manteniendo la seguridad y eficiencia en la comunicación entre sistemas.

En resumen, AIssistant es un sistema inteligente diseñado para proporcionar una experiencia fluida de interacción, con características avanzadas como la gestión de usuarios y acceso controlado, integraciones eficientes mediante FastAPI y un modelo de procesamiento de lenguaje natural de última generación.
