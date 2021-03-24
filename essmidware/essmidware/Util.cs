using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Script.Serialization;

namespace ess.midware.essharp
{
    class Util
    {
        public static string JsonSerialize(Dictionary<string, object> dict)
        {

            JavaScriptSerializer serializer = new JavaScriptSerializer();

            return serializer.Serialize(dict);
        }
    }
}
