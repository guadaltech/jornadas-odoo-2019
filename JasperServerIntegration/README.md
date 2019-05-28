### Introducción
Este repositorio contiene el módulo de Odoo que permite la integración entre Odoo 11 con un servidor de impresión de informes de Jasper Server.

Esta documentación contiene información sobre el módulo implementado y sobre cómo desplegar la infraestructura para poder usar este módulo.

### Uso del módulo
## Configuración en Jasper Server
Para entrar en el sistema de Jasper Server, debemos acceder a la página de login, que generalmente usa el formato: "http://<host>:8080/jasperserver/". Una vez iniciemos sesión con los credenciales obtenidos (o "jasperadmin/jasperadmin"/"user/bitnami" dependiendo de la distribucción usada) tendremos acceso al repositorio de Jasper Server. El repositorio contiene todos los objetos necesarios para crear e imprimir informes. 

Para crear un informe, primero debemos acceder a Jasper Server. Creamos el informe en la carpeta "Reports" accediendo a la carpeta, realizando click derecho en la carpeta y seleccionando "Add Resource/JasperReport".

Los datos a rellenar para crear el informe son los siguientes:
 - "Name": El nombre del informe. Lo usaremos después para indicar su impresión por Odoo.
 - "Description": Opcionalmente, podemos indicar qué hace este informe en ese campo.
 - "JRXML": Indicar el archivo JRXML inicial, que contendrá los posibles subinformes. Podemos seleccionar tanto uno de nuestro equipo como uno ya subido al repositorio seleccionando la otra opción.
 - "Resources": Debemos indicar las rutas a imágenes, estilos y archivos JARs aqui.
 - "Input Controls": Controlará los parámetros introducidos desde Odoo y permitirá comunicación entre ambos sistemas. Se describe la creación de este tipo de objetos:
   - Salvo que se trate de un Input Control ya existente, la mayoría de las veces tendremos que crearlo desde cero, por lo que seleccionamos "Define an Input Control in the next step". 
   - En esta pestaña seleccionamos qué tipo de valores podrán introducirse. Para valores como ids o textos, dejaremos el elemento "Single Value" mientras que si queremos un conjunto de posibles valores, seleccionamos "Single-Select List of Values". También es posible introducir la propia Query que se ejecutará por base de datos. Debemos también rellenar el nombre del parámetro (que nos permitirá obtenerlo en el informe) así como si es necesario ("Mandatory") o de sólo lectura ("Read-only").
   - En la siguiente pestaña, declararemos el tipo de valores que pueden introducirse en el Input Control. Se recomienda tener objetos preparados para algunos tipos comunes como Ids, Texto y otros en la carpeta "Resources", que permitirá reducir gran parte de la configuración inicial.
   - Cuando necesitemos crear un nuevo objeto, debemos tener en cuenta en el primer selector el tipo de valores aceptados ("Text", "Number"...). Y los valores mínimos y máximos.
  - En "Data Source", salvo que no configuremos nosotros mismos en el informe la conexión con la base de datos, debemos fijarlo con "Select data source from repository" y acceder a la carpeta "Datasources".
  - Finalmente, podemos indicar la query a operar en el informe. Este valor se recomienda realizar en el editor de informes que usemos, ya que aporta funcionalidades más útiles para obtener valores de la base de datos.

Siguiendo estos pasos, podremos guardar el informe ("Submit") y lo tendremos preparado por Jasper Server para su impresión. Podemos incluso probarlo a través de Jasper Server con la acción "Run" sobre el informe.

## Configuración en Odoo
Una vez tengamos el informe listo en Jasper Server, debemos crear el informe en Odoo para que apunte al informe creado. Para ello, accedemos a la distribucción de Odoo correspondiente y activamos el modo desarrollador, que nos permitirá acceder al menú de informes. Una vez dentro, debemos fijarnos en el nuevo menú añadido, llamado "Jasper Server Configuration" que permite configurar el acceso al servidor. En este menú, definimos la URL del servidor (siguiendo el esquema determinado) así como los credenciales del usuario de Jasper Server que imprimirá los informes. Una vez se disponga de la configuración del servidor hecha, se podrán crear informes.

Para crear un informe, se accederá a la vista de informes. En esta vista, se configurará como tipo de informe uno con tipo "PDF" y se seleccionará el checkbox de "¿Es un informe de Jasper Server?". En la pestaña de "Jasper Server Settings" se podrá configurar la ruta (que consiste en la ruta desde la raiz del repositorio). Los parámetros también se podrán fijar según un trozo de código de Python. 

Cuando se termine el informe, se puede asignar como disponible para imprimir haciendo click en el botón superior derecho ("Añadir al menú de impresión").

### Configuración de la infraestructura de Jasper Server
## Introducción
Gran parte de la información de esta sección proviene de la documentación oficial de Jasper Server, que puede encontrarse [en esta página](https://community.jaspersoft.com/documentation/tibco-jasperreports-server-installation-guide/v630/introduction).

## Pre instalación
Para instalar Jasper Server, debe instalarse previamente las siguientes dependencias:
 - Una versión de Java (OpenJDK o Oracle) posterior a la versión 1.8.
 - (Opcional, si quiere instalarse con un Apache Tomcat de base) Apache Tomcat (versiones 6, 7 u 8).
 - (Opcional, si quiere instalarse de base) Una base de datos. Existen varias distribucciones válidas:
   - PostgreSQL, MySQL, Oracle y SQL Server: La instalación de Jasper Server contiene los drivers JDBC necesarios, aunque pueden instalarse por separado.
   - DB2: Necesario realizar los pasos de la [documentación](https://community.jaspersoft.com/documentation/tibco-jasperreports-server-installation-guide/v630/additional-steps-using-db2-and-js).
 - (Opcional, si quiere instalarse de base) PhantomJS con la última versión.

Cabe destacar que los ítems opcionales sólo serán aplicables si no se usa el instalador automático. La instalación desde base se asume que partirá con un Apache Tomcat preparado y una de las bases de datos mencionadas anteriormente. La base de datos no puede ser la misma que la de Odoo, debido a la creación de datos temporales que podrían producir problemas.

## Instalación
Existen 2 maneras de instalar Jasper Server.

# Instalación automática
Por un lado, se puede instalar Jasper Server con un instalador automático, que instalará las dependencias mencionadas como opcionales en el anterior paso. El instalador automático puede encontrarse en el siguiente [vínculo](https://community.jaspersoft.com/project/jasperreports-server/releases). Este instalador se recomienda que se aplique a instalaciones locales por parte de un encargado, ya que debe realizarse de forma interactiva.

# Instalación manual
Por otro lado, se puede instalar Jasper Server como una 'webapp' de Apache Tomcat. Para aplicar esta instalación, se necesitan todas las dependencias mencionadas anteriormente.

El archivo que contiene la instalación de Jasper Server se puede descargar en la anterior página y debe contener '-bin' como nombre del archivo. Se debe descomprimir y debe configurarse la conexión a la base de datos. La configuración de ejemplo para la base de datos puede encontrarse en la carpeta "sample_conf" de la carpeta descomprimida y se deben seguir los comentarios indicados. Como ejemplo de una configuración que usa la base de datos de PostgreSQL, se describen los pasos a seguir para configurar la conexión con la base de datos:

 1. Cambiar en "appServerType" (linea 56) según el tipo de lanzador de aplicaciones Java usado, en este caso dejar como "tomcat".
 2. Cambiar la localización del Apache Tomcat según la instalación realizada cambiando el valor de "appServerDir" (linea 64). En el caso de haber instalado Apache Tomcat a través de un gestor de aplicaciones, debe asignarse la localización de Catalina descomentando la variable "CATALINA_HOME" y "CATALINA_BASE". 
 3. "dbType" (linea 81) debe mantenerse como "postgresql". En el caso de usarse MySQL, debe usarse el otro archivo de configuración de "sample_conf".
 4. En "dbHost", "dbUsername" y "dbPassword" cambiar a la configuración apropiada de la base de datos.
 5. Finalmente, se debería configurar "dbPort" (linea 93) en el caso de ser necesario.

Una vez se tenga la configuración lista, se copiará el archivo de configuración y se pondrá en la carpeta "buildomatic". Para instalar Jasper Server, ejecutamos 'js-install-ce.sh' con bash (importante).

Se dispondrá el 'webapp' en Apache Tomcat, siendo accesible a través del puerto 8080 y se puede iniciar sesión con "jasperadmin/jasperadmin".

## Configuración inicial
Para conseguir que el módulo de Odoo pueda funcionar correctamente con Jasper Server, es necesario preparar antes un "Data Source", que consiste en una configuración para el conector de la base de datos. 

Antes de crear el Data Source, se recomienda disponer las carpetas del repositorio (que es la carpeta compartida del sistema) de Jasper Server de la siguiente forma:

 - Root:
   - Datasources: Contendrá las diferentes fuentes de bases de datos. Existen otros conectores para poder usar diferentes fuentes.
   - Reports: Esta carpeta contendrá los informes. Pueden crearse subcarpetas para separar mejor los informes.
   - Resources: Esta carpeta contendrá las imágenes, estilos, JARs y otros elementos auxiliares. Pueden asociarse al informe en la creación del informe.
   
Para crear un Data Source, debemos acceder a la carpeta correspondiente en el panel de la izquierda, hacer click derecho en la carpeta donde queramos ponerla y seleccionar "Add Resource/Datasource". Esto abrirá la configuración del Datasource. Los principales atributos a configurar son
 - "JDBC Driver" (permite seleccionar otras distribucciones de SGBD, pero por defecto es PostgreSQL)
 - "Host" (la URL que identifica al equipo con el SGBD), "Port" (el puerto por el que escucha la SGBD) 
 - "Database" (el nombre de la base de datos, la mayoría de las veces será "odoo")
 - "URL" (URL completa que indica la localización del SGBD y la base de datos seleccionada. Debe cumplimentarse con los otros datos)
 - "User name" (Nombre del usuario del SGBD, debemos poner los credenciales que se usan para acceder a Odoo o usar un usuario con permisos de lectura del esquema público).
 - "Password" (igual que el nombre del usuario).
 - Se indica que al usar la última versión del conector de PostgreSQL, existe un método deprecado usado por Jasper Server que lanza error. Esto significa que la prueba de la conexión en este menú no funciona.

Finalmente, se recomienda el uso de un usuario que creara informes. Para crear un usuario, debemos seleccionar la pestaña "Manage" del menú de arriba y acceder a "Users". Se puede crear usuarios con "Add User..." así como crear roles en la sección de "Roles" de "Manage".