using System.Collections.Generic;
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
