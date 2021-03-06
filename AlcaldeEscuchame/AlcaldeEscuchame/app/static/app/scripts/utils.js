
/**
 * Función que devuelve un Pop-Up de confirmación para la eliminación de un objeto.
 */
function confirmaAccion(accion) {
    var mensaje = "";

    switch (accion) {
        case 'elimina-queja':
            mensaje = "Va a eliminar la queja seleccionada. Si desea continuar, pulse aceptar.";
            break;

        case 'tramita-queja':
            mensaje = "Va a tramitar la queja seleccionada. Si desea continuar, pulse aceptar.";
            break;

        case 'agrega-queja-corpus':
            mensaje = "Va a crear una nueva entrada para el corpus del sistema con los datos de esta queja. Si desea continuar, pulse aceptar."
            break;

        default:
            mensaje = "";
    }        

    var res = confirm(mensaje);

    if (res) {
        return true;
    } else {
        return false
    }
}