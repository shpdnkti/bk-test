/**
 * @file ajax response
 * @author ielgnaw <wuji0223@gmail.com>
 */

export function response(getArgs, postArgs, req) {

    const method = req.method;

    const ret = method.toUpperCase() === 'GET'
        ? {
            count: getArgs.count,
            getArgs: getArgs,
            method: 'get'
        }
        : {
            count: postArgs.count,
            postArgs: postArgs,
            method: 'post'
        }

    return {
        status: 0,
        msg: 'ζδΊ€ζε',
        data: ret
    };
};
