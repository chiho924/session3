"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


# TODO: Add functions for handling more arithmetic operations.


def add(*args):
    """
    Returns a STRING with the sum of the arguments

    :param args: the list of two operands of the addition operation
    :return a String with the sum of the operands
    """

    # Add the two operands.
    sum = int(args[0]) + int(args[1])

    return str(sum)


def subtract(*args):
    """
    Returns a STRING with the difference of the arguments.

    :param args: the list of two operands of the subtraction operation
    :return: a String with the difference of the operands
    """

    # Subtract the two operands.
    difference = int(args[0]) - int(args[1])

    return str(difference)


def multiply(*args):
    """
    Returns a STRING with the product of the arguments.

    :param args: the list of two operands of the multiplication operation
    :return: a String with the product of the operands.
    """

    # Multiply the two operands.
    product = int(args[0]) * int(args[1])

    return str(product)


def divide(*args):
    """
    Returns a STRING with the quotient of the arguments.

    :param args: the list of two operands of the division operation
    :return: a String with the quotient of the operands
    """

    if int(args[1]) != 0:  # Make sure that there is no division by zero.
        quotient = int(args[0]) / int(args[1])
        return str(quotient)
    else: # Division by zero
        raise ZeroDivisionError


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    # Get the parameters from the path.
    parameters = path.strip('/').split('/')

    if len(parameters) <= 1:  # No operands in the path
        func = None
        args = None
    else:

        # Determine the operation type (e.g., add, subtract, multiply or divide).
        if parameters[-3] == 'add':
            func = add
        elif parameters[-3] == 'subtract':
            func = subtract
        elif parameters[-3] == 'multiply':
            func = multiply
        elif parameters[-3] == 'divide':
            func = divide
        else:
            raise NameError  # invalid operation type

        # Get the two operands from the parameters list.
        args = [parameters[-2], parameters[-1]]

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)

        if func is None and func is None: # Display how to use this page.
            body = """ <!DOCTYPE html>
            <html>
            <head>
            <title>Python 200: Assignment 3 - Calculator</title>
            </head>
            <body>
            <h1>Python 200</h1>
            <h2>Assignment 3: WSGI Calculator</h2>
            <p>Here is how to use this page</p>
            <ol>
            <li>http://localhost:8080/add/23/42 => 65</li>
            <li>http://localhost:8080/subtract/23/42 => -19</li>
            <li>http://localhost:8080/multiply/3/5 => 15</li>
            <li>http://localhost:8080/divide/22/11 => 2</li>
            <li>http://localhost:8080/divide/6/0 => HTTP "400 Bad Request"</li>
            <li>http://localhost:8080/ => Manual</li>
            </ol>
            </body>
            </html>"""
        else:
            body = func(*args)
        status = "200 OK"
    except ZeroDivisionError:  # division by zero
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
    except ValueError:  # invalid operand type (i.e., non-numeric operand type)
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except NameError:  # invalid operation type
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:  # other general run-time exceptions
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()